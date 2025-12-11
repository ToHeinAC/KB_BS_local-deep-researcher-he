import sys
import os

# Add project root to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

print("Testing App Dependencies...")

try:
    print("1. Testing src.state...")
    from src.state import ResearcherState, HitlState
    print("   OK")

    print("2. Testing src.graph...")
    from src.graph import create_hitl_graph, create_main_graph
    print("   OK")

    print("3. Testing src.configuration...")
    from src.configuration import get_config_instance
    print("   OK")

    print("4. Testing src.vector_db...")
    from src.vector_db import get_embedding_model_path, get_vector_db_path, SPECIAL_DB_CONFIG
    print("   OK")

    print("5. Testing src.rag_helpers...")
    from src.rag_helpers import get_report_llm_models, get_summarization_llm_models, get_license_content
    print("   OK")
    
    print("ALL DEPENDENCIES IMPORTED SUCCESSFULLY")

except ImportError as e:
    print(f"IMPORT ERROR: {e}")
    sys.exit(1)
except Exception as e:
    print(f"ERROR: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
