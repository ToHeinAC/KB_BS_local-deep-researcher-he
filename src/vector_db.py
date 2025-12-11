import os
import logging
from typing import List
# Use updated import path to avoid deprecation warning
try:
    from langchain_huggingface import HuggingFaceEmbeddings
except ImportError:
    # Fallback to original import if package is not installed
    from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.document_loaders import DirectoryLoader
from langchain_chroma import Chroma
from langchain_core.documents import Document

# Base path for vector database
VECTOR_DB_PATH = "database"
DEFAULT_TENANT_ID = "default"

# Define the special database configuration
SPECIAL_DB_CONFIG = {
    'sentence-transformers--paraphrase-multilingual-MiniLM-L12-v2--2000--400': {
        'tenant_id': '2025-04-22_15-41-10',
        'collection_name': 'collection_2025-04-22_15-41-10'
    }
}

def get_embedding_model():
    """Get the embedding model."""
    from src.configuration import get_config_instance
    
    # Get the embedding model from the global configuration instance
    embedding_model_name = get_config_instance().embedding_model
    
    emb_model = HuggingFaceEmbeddings(model_name=embedding_model_name, model_kwargs={'device': 'cpu'})
    print('-------------------------')
    print(f"Using embedding model: {embedding_model_name}")
    print(emb_model)
    print('-------------------------')
    return emb_model

def get_embedding_model_path():
    """Get the sanitized embedding model name for use in paths."""
    from src.configuration import get_config_instance
    
    # Get the embedding model from the global configuration instance
    embedding_model_name = get_config_instance().embedding_model
    
    # Create a sanitized version of the model name for folder paths
    sanitized_model_name = embedding_model_name.replace('/', '--')
    
    return sanitized_model_name

def get_vector_db_path():
    """Get the vector database path including the embedding model name."""
    sanitized_model_name = get_embedding_model_path()
    return os.path.join(VECTOR_DB_PATH, sanitized_model_name)

def get_tenant_collection_name(tenant_id):
    """Get the collection name for a tenant."""
    return f"collection_{tenant_id}"

def get_tenant_vectorstore(tenant_id, embed_llm, persist_directory, similarity, normal=True):
    """Get the vector store for a tenant."""
    # Get tenant-specific directory
    tenant_vdb_dir = os.path.join(persist_directory, tenant_id)
    
    # Create directory if it doesn't exist
    os.makedirs(tenant_vdb_dir, exist_ok=True)
    
    # Get collection name for tenant
    collection_name = get_tenant_collection_name(tenant_id)
    
    return Chroma(
        persist_directory=tenant_vdb_dir,
        collection_name=collection_name,
        embedding_function=embed_llm,
        collection_metadata={"hnsw:space": similarity, "normalize_embeddings": normal}
    )

def search_documents(query: str, k: int = 3, language: str = "English") -> List[Document]:
    """
    Search for documents in the vector database.
    
    Args:
        query: The search query.
        k: Number of documents to retrieve.
        language: Language of the query.
        
    Returns:
        List of retrieved Documents.
    """
    
    # Set up logging
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)
    
    # Clear CUDA memory before embedding
    from src.utils import clear_cuda_memory
    clear_cuda_memory()
    
    # Get the configured embedding model
    embeddings = get_embedding_model()
    
    # Get the selected database from configuration
    from src.configuration import get_config_instance
    config = get_config_instance()
    selected_database = config.selected_database
    
    # Use absolute path for database
    # Database is located in kb/database folder relative to the project root
    # Project root is ../ from src/
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    DATABASE_PATH = os.path.join(project_root, 'kb', 'database')
    
    if selected_database:
        # Use the selected database from the UI
        vector_db_path = os.path.join(DATABASE_PATH, selected_database)
        logger.info(f"Using selected database: {selected_database}")
        logger.info(f"Database path: {vector_db_path}")
        
        # Check if it's a special configuration
        special_db_key = None
        for key in SPECIAL_DB_CONFIG.keys():
            if key in selected_database:
                special_db_key = key
                break
        
        if special_db_key:
            tenant_id = SPECIAL_DB_CONFIG[special_db_key]['tenant_id']
            collection_name = SPECIAL_DB_CONFIG[special_db_key]['collection_name']
            logger.info(f"Using special configuration - tenant: {tenant_id}, collection: {collection_name}")
        else:
            tenant_id = DEFAULT_TENANT_ID
            collection_name = None
            logger.info(f"Using default configuration - tenant: {tenant_id}")
    else:
        # Fallback to embedding model-based path (legacy)
        current_embedding_model = config.embedding_model
        sanitized_model_name = current_embedding_model.replace('/', '--')
        
        # Try to find matching database directory
        available_dbs = []
        if os.path.exists(DATABASE_PATH):
            available_dbs = [d for d in os.listdir(DATABASE_PATH) 
                           if os.path.isdir(os.path.join(DATABASE_PATH, d))]
        
        # Find database that contains the embedding model name
        matching_db = None
        for db in available_dbs:
            if sanitized_model_name in db:
                matching_db = db
                break
        
        if matching_db:
            vector_db_path = os.path.join(DATABASE_PATH, matching_db)
            logger.info(f"Found matching database: {matching_db}")
        else:
            vector_db_path = os.path.join(DATABASE_PATH, sanitized_model_name)
            logger.info(f"Using fallback DB path: {vector_db_path}")
        
        tenant_id = DEFAULT_TENANT_ID
        collection_name = None
    
    try:
        # Similarity search logic
        clear_cuda_memory()
        
        tenant_vdb_dir = os.path.join(vector_db_path, tenant_id)
        
        if not os.path.exists(tenant_vdb_dir):
            error_msg = f"Vector database directory for tenant {tenant_id} does not exist at {tenant_vdb_dir}"
            logger.error(error_msg)
            # Try finding any directory if the specific tenant doesn't exist? 
            # Reference implementation threw exception. We might want to be graceful.
            return []

        if collection_name is None:
            collection_name = get_tenant_collection_name(tenant_id)
            
        vectorstore = Chroma(
            persist_directory=tenant_vdb_dir,
            collection_name=collection_name,
            embedding_function=embeddings,
            collection_metadata={"hnsw:space": "cosine", "normalize_embeddings": True}
        )
        
        logger.info(f"Executing similarity_search with query: '{query}' and k={k}")
        results = vectorstore.similarity_search(query, k=k)
        logger.info(f"Retrieved {len(results)} documents from search")
        
        # Add language metadata
        for doc in results:
            if "metadata" in doc.__dict__:
                doc.metadata["language"] = language
                
        # Clean up
        vectorstore = None
        clear_cuda_memory()
        
        return results
        
    except Exception as e:
        logger.error(f"Error searching for documents: {e}")
        clear_cuda_memory()
        return []
