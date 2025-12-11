import os
import re
from typing import List, Dict, Any
from langchain_core.messages import SystemMessage, HumanMessage
from langchain_community.llms import Ollama
from src.prompts import SUMMARIZER_SYSTEM_PROMPT, SUMMARIZER_HUMAN_PROMPT

def load_models_from_file(file_path: str) -> List[str]:
    """
    Load model names from a markdown file.
    """
    if not os.path.exists(file_path):
        return []
    
    models = []
    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith('#'):
                models.append(line)
    return models

def get_llm_models() -> List[str]:
    """
    Get the list of available LLM models from LLM_Choice.md.
    """
    current_dir = os.path.dirname(os.path.abspath(__file__))
    llm_choice_path = os.path.join(current_dir, 'LLM_Choice.md')
    
    models = load_models_from_file(llm_choice_path)
    if not models:
        return [
            "gpt-oss:20b",
            "ministral-3:14b"
        ]
    return models

def get_report_llm_models() -> List[str]:
    """
    Get the list of available report LLM models (deprecated - use get_llm_models).
    """
    return get_llm_models()

def get_summarization_llm_models() -> List[str]:
    """
    Get the list of available summarization LLM models (deprecated - use get_llm_models).
    """
    return get_llm_models()

def extract_embedding_model(db_dir_name):
    """
    Extract the embedding model name from the database directory name.
    """
    # Handle the specific case of database names with '__' and '--' separators
    if '__' in db_dir_name:
        parts = db_dir_name.split('__')
        if len(parts) >= 2:
            model_info = parts[1]
            if '--' in model_info:
                model_parts = model_info.split('--')
                if len(model_parts) >= 2:
                    org = model_parts[0]
                    model_name = model_parts[1]
                    return f"{org}/{model_name}"
            
            path_prefix = parts[0]
            if '/' in path_prefix:
                org = path_prefix.split('/')[0]
            else:
                org = "unknown"
            return f"{org}/{model_info}"
    
    elif '--' in db_dir_name:
        parts = db_dir_name.split('--')
        if len(parts) >= 2:
            first_part = parts[0]
            second_part = parts[1]
            if '/' in first_part:
                org = first_part.split('/')[0]
                return f"{org}/{second_part}"
            else:
                return f"{first_part}/{second_part}"
    
    model_name = db_dir_name.replace("vectordb_", "")
    model_name = model_name.replace("--", "/")
    return model_name

def source_summarizer_ollama(user_query, context_documents, language, system_message, llm_model="deepseek-r1", human_feedback=""):
    print(f"Generating summary using language: {language}")
    print(f"  [DEBUG] Actually using summarization model in source_summarizer_ollama: {llm_model}")
    
    if not language or not isinstance(language, str):
        language = "English"
    
    try:
        system_message = SUMMARIZER_SYSTEM_PROMPT.format(language=language)
    except Exception as e:
        print(f"  [ERROR] Error formatting system prompt with language '{language}': {str(e)}")
        language = "English"
        system_message = SUMMARIZER_SYSTEM_PROMPT.format(language=language)

    if isinstance(context_documents, str):
        formatted_context = context_documents
    else:
        try:
            formatted_context = "\n".join(
                f"Content: {doc.page_content}\nSource: {doc.metadata.get('source', 'Unknown')}\nPath: {doc.metadata.get('path', 'Unknown')}"
                for doc in context_documents
            )
        except (TypeError, AttributeError):
            formatted_context = str(context_documents)

    prompt = SUMMARIZER_HUMAN_PROMPT.format(
        user_query=user_query,
        documents=formatted_context,
        human_feedback=human_feedback,
        language=language
    )
    
    llm = Ollama(model=llm_model, temperature=0.1, repeat_penalty=1.2) 
    
    messages = [
        SystemMessage(content=system_message),
        HumanMessage(content=prompt)
    ]
    
    response = llm.invoke(messages)
    
    # Clean markdown formatting if present
    try:
        final_content = re.sub(r"<think>.*?</think>", "", response, flags=re.DOTALL).strip()
    except:
        final_content = response.strip()

    return final_content

def linkify_sources(text, selected_database=None, kb_path="./kb"):
    """
    Convert source references like [Filename.pdf] to clickable links or base64 data URIs.
    For this implementation, we will keep it simple and just return the text, 
    or basic markdown links if we can resolve them.
    """
    # This is a simplified placeholder. 
    # The full implementation requires resolving PDF paths and potentially creating base64 data URIs
    # which is UI specific. 
    return text

def get_license_content() -> str:
    """
    Get the content of the LICENSE file for display in the applications.
    
    Returns:
        str: The content of the LICENSE file
    """
    # Get the path to the LICENSE file (one level up from src)
    current_dir = os.path.dirname(os.path.abspath(__file__))
    license_path = os.path.join(os.path.dirname(current_dir), 'LICENCE')
    
    try:
        with open(license_path, 'r', encoding='utf-8') as f:
            return f.read().strip()
    except FileNotFoundError:
        return "Apache License 2.0 - License file not found"
