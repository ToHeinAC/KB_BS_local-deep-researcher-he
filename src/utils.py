import os
import re
import shutil
import json
import torch
from ollama import chat
from tavily import TavilyClient
from pydantic import BaseModel
from typing import List, Dict, Any, Optional

class DetectedLanguage(BaseModel):
    language: str

class Queries(BaseModel):
    queries: List[str]

def clear_cuda_memory():
    """
    Clear CUDA memory cache to free up GPU resources between queries.
    Only has an effect if CUDA is available.
    """
    if torch.cuda.is_available():
        # Empty the cache
        torch.cuda.empty_cache()
        
        # Force garbage collection
        import gc
        gc.collect()
        
        print("CUDA memory cache cleared")
    return

def get_configured_llm_model(default_model='deepseek-r1:latest'):
    return os.environ.get('LLM_MODEL', default_model)

def invoke_ollama(model, system_prompt, user_prompt, output_format=None):
    # Use the configured model if none is specified
    if model is None:
        model = get_configured_llm_model()
    
    print(f"  [DEBUG] Actually using model in invoke_ollama: {model}")
        
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt}
    ]
    
    try:
        response = chat(
            messages=messages,
            model=model,
            format=output_format.model_json_schema() if output_format else None
        )
        
        if not response or not response.message or not response.message.content:
            error_msg = f"Error: The LLM model {model} returned an empty response."
            print(f"  [ERROR] {error_msg}")
            raise ValueError(error_msg)
        
        content = response.message.content
        
        if not content.strip():
            error_msg = f"Error: The LLM model {model} returned an empty response."
            print(f"  [ERROR] {error_msg}")
            raise ValueError(error_msg)

        if output_format:
            return output_format.model_validate_json(content)
        else:
            return content
            
    except Exception as e:
        if "returned an empty response" in str(e):
            raise
        print(f"  [ERROR] Exception in invoke_ollama with model {model}: {str(e)}")
        raise Exception(f"Error invoking model {model}: {str(e)}") from e

def parse_output(text):
    """
    Parse LLM output, extracting thinking blocks (<think>...</think>) and handling JSON responses.
    """
    # First try to extract thinking part if it exists
    think_match = re.search(r'<think>(.*?)</think>', text, re.DOTALL)
    
    if think_match:
        think = think_match.group(1).strip()
        output = re.search(r'</think>\s*(.*?)$', text, re.DOTALL).group(1).strip()
    else:
        think = None
        output = text.strip()
    
    # Check if the output is in JSON format with key-value pairs
    try:
        # Check if the text looks like JSON
        if (output.startswith('{') and output.endswith('}')) or (output.startswith('[') and output.endswith(']')):
            # Try to parse as JSON
            json_obj = json.loads(output)
            
            # If it's a dict with a 'final_answer' or similar key, extract just the value
            if isinstance(json_obj, dict):
                # Look for common keys that might contain the main content
                for key in ['final_answer', 'answer', 'response', 'content', 'result', 'output']:
                    if key in json_obj:
                        output = json_obj[key]
                        break
                # If no specific key was found but there's only one value, use that
                if len(json_obj) == 1:
                    output = list(json_obj.values())[0]
    except (json.JSONDecodeError, ValueError, AttributeError):
        # If it's not valid JSON or any other error occurs, keep the original output
        pass
    
    return {
        "reasoning": think,
        "response": output
    }

def tavily_search(query, include_raw_content=True, max_results=3):
    """ Search the web using the Tavily API. """
    tavily_client = TavilyClient()
    return tavily_client.search(
        query,
        max_results=max_results,
        include_raw_content=include_raw_content
    )

def format_documents_with_metadata(documents, preserve_original=False):
    formatted_docs = []
    for doc in documents:
        # Get the source filename from metadata
        source = doc.metadata.get('source', 'Unknown source')
        
        # Ensure we have an absolute path to the document
        doc_path = ''
        if 'path' in doc.metadata and os.path.isfile(doc.metadata['path']):
            doc_path = doc.metadata['path']
        elif 'source' in doc.metadata:
            # Try to construct an absolute path to the file in the files directory
            potential_path = os.path.abspath(os.path.join(os.getcwd(), 'files', source))
            if os.path.isfile(potential_path):
                doc_path = potential_path
            else:
                doc_path = os.path.abspath(os.path.join(os.getcwd(), 'files', source))
        
        # Extract just the filename for display
        filename = os.path.basename(source) if source != 'Unknown source' else 'Unknown source'
        
        # Format with markdown link
        if doc_path:
            if '/files/' not in doc_path and '\\files\\' not in doc_path:
                files_dir = os.path.join(os.getcwd(), 'files')
                doc_path = os.path.join(files_dir, filename)
            source_link = f"[{filename}]({doc_path})"
        else:
            files_dir = os.path.join(os.getcwd(), 'files')
            doc_path = os.path.join(files_dir, filename)
            source_link = f"[{filename}]({doc_path})"
        
        if preserve_original:
            formatted_doc = f"SOURCE: {source_link}\n\nContent: {doc.page_content}"
        else:
            formatted_doc = f"SOURCE: {source_link}\n\nContent: {doc.page_content}"
            
        formatted_docs.append(formatted_doc)
    return "\n\n---\n\n".join(formatted_docs)
