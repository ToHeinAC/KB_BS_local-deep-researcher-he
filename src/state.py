import operator
from typing import Annotated, List, Dict, Any, Optional
from typing_extensions import TypedDict
from langchain_core.documents import Document

class ResearcherState(TypedDict):
    """
    State for the Deep Researcher graph.
    """
    # Input
    user_query: str
    
    # HITL / Context Management
    detected_language: str
    human_feedback: str
    additional_context: str
    
    # Planning & Task Decomposition
    research_queries: List[str]  # List of sub-questions/tasks
    
    # Execution / Subagent Outputs
    # We aggregate documents from all sub-tasks
    retrieved_documents: Dict[str, List[Document]] 
    search_summaries: Dict[str, List[Document]]
    
    # Web Search (Optional)
    web_search_enabled: bool
    internet_result: Optional[str]
    
    # Reporting
    final_answer: str
    linked_final_answer: Optional[str]
    
    # Quality Assurance
    quality_check: Optional[Dict[str, Any]]
    reflection_count: int
    enable_quality_checker: bool
    
    # Configuration
    report_llm: str
    summarization_llm: str
    selected_database: Optional[str]

class HitlState(TypedDict):
    """
    State for the Human-in-the-Loop (HITL) process.
    """
    user_query: str
    current_position: int
    detected_language: str
    additional_context: str
    human_feedback: str
    analysis: str
    follow_up_questions: str
    report_llm: str
    summarization_llm: str
    research_queries: List[str]
    max_search_queries: int
