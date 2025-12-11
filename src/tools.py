from langchain_core.tools import tool
from typing import List, Dict, Any, Optional
from src.vector_db import search_documents
from src.utils import tavily_search, parse_output
from src.rag_helpers import source_summarizer_ollama, extract_embedding_model
from src.configuration import get_config_instance
from src.prompts import (
    LLM_QUALITY_CHECKER_SYSTEM_PROMPT, 
    LLM_QUALITY_CHECKER_HUMAN_PROMPT,
    REPORT_WRITER_SYSTEM_PROMPT,
    REPORT_WRITER_HUMAN_PROMPT
)
from src.utils import invoke_ollama
from langchain_core.documents import Document

@tool
def vector_db_retriever_tool(query: str, k: int = 3, language: str = "English") -> List[Document]:
    """
    Retrieve documents from the local vector database based on a query.
    
    Args:
        query: The search query.
        k: Number of documents to retrieve.
        language: Language of the query.
        
    Returns:
        List of retrieved Documents.
    """
    return search_documents(query=query, k=k, language=language)

@tool
def web_search_tool(query: str, max_results: int = 3) -> str:
    """
    Search the internet for information.
    
    Args:
        query: The search query.
        max_results: Maximum number of results to return.
        
    Returns:
        Formatted search results string.
    """
    config = get_config_instance()
    if not config.enable_web_search:
        return "Web search is disabled in configuration."
        
    try:
        results = tavily_search(query=query, max_results=max_results)
        # Simple formatting of results
        formatted = ""
        for i, res in enumerate(results.get('results', [])):
            formatted += f"Source {i+1}: {res.get('title', 'Unknown Title')}\n"
            formatted += f"URL: {res.get('url', 'Unknown URL')}\n"
            formatted += f"Content: {res.get('content', '')}\n\n"
        return formatted if formatted else "No results found."
    except Exception as e:
        return f"Error performing web search: {str(e)}"

@tool
def document_summarizer_tool(query: str, documents: List[Document], language: str = "English") -> str:
    """
    Summarize a list of documents in the context of a query.
    
    Args:
        query: The user query.
        documents: List of documents to summarize.
        language: Output language.
        
    Returns:
        Summarized text.
    """
    config = get_config_instance()
    return source_summarizer_ollama(
        user_query=query,
        context_documents=documents,
        language=language,
        system_message="", # handled inside function
        llm_model=config.summarization_llm
    )

@tool
def quality_checker_tool(final_answer: str, summaries: str, original_query: str, language: str = "English") -> Dict[str, Any]:
    """
    Check the quality of the final report against source summaries.
    
    Args:
        final_answer: The generated report.
        summaries: The source summaries used.
        original_query: The user's original query.
        language: Language for the critique.
        
    Returns:
        JSON dictionary with quality assessment.
    """
    config = get_config_instance()
    
    system_prompt = LLM_QUALITY_CHECKER_SYSTEM_PROMPT.format(language=language)
    human_prompt = LLM_QUALITY_CHECKER_HUMAN_PROMPT.format(
        final_answer=final_answer,
        all_reranked_summaries=summaries, # Assuming string or stringified list
        query=original_query,
        language=language
    )
    
    try:
        response = invoke_ollama(
            model=config.report_llm,
            system_prompt=system_prompt,
            user_prompt=human_prompt
        )
        return parse_output(response).get("response", {})
    except Exception as e:
        return {"error": str(e), "quality_score": 0, "is_accurate": False, "improvement_needed": True}

@tool
def final_report_generator_tool(user_query: str, information: str, structure: str, language: str = "English") -> str:
    """
    Generate the final report.
    
    Args:
        user_query: The original user query.
        information: aggregated summaries and info.
        structure: The report structure template.
        language: Output language.
        
    Returns:
        The generated report markdown.
    """
    config = get_config_instance()
    
    system_prompt = REPORT_WRITER_SYSTEM_PROMPT.format(language=language)
    human_prompt = REPORT_WRITER_HUMAN_PROMPT.format(
        instruction=user_query,
        information=information,
        report_structure=structure,
        language=language
    )
    
    return invoke_ollama(
        model=config.report_llm,
        system_prompt=system_prompt,
        user_prompt=human_prompt
    )
