import os
from typing import Optional, List, Dict, Any
from dotenv import load_dotenv
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_core.tools import tool
from langgraph.prebuilt import create_react_agent
from langchain_ollama import ChatOllama
from langchain_core.messages import HumanMessage, SystemMessage

# Load environment variables
load_dotenv()

# Configuration
LLM_MODEL = "gpt-oss:20b"
# LLM_MODEL = "deepseek-r1:latest" # Fallback

# Global state for todo list (shared across tool calls)
_todo_list: List[Dict[str, Any]] = []

def get_llm(temperature: float = 0.3):
    """Get the configured LLM instance."""
    return ChatOllama(model=LLM_MODEL, temperature=temperature)

# --- Todo List Tools ---

@tool
def create_todo(task: str, priority: str = "medium") -> str:
    """
    Create a new todo item in your research plan.
    ALWAYS use this tool first to plan your research before searching.
    
    Args:
        task: Description of the research task to complete.
        priority: Priority level - 'high', 'medium', or 'low'. Defaults to 'medium'.
    """
    global _todo_list
    todo_id = len(_todo_list) + 1
    todo = {
        "id": todo_id,
        "task": task,
        "priority": priority,
        "status": "pending"
    }
    _todo_list.append(todo)
    return f"Created todo #{todo_id}: {task} (priority: {priority})"

@tool
def update_todo(todo_id: int, status: str) -> str:
    """
    Update the status of a todo item.
    Use this to mark tasks as 'in_progress' or 'completed'.
    
    Args:
        todo_id: The ID of the todo item to update.
        status: New status - 'pending', 'in_progress', or 'completed'.
    """
    global _todo_list
    for todo in _todo_list:
        if todo["id"] == todo_id:
            todo["status"] = status
            return f"Updated todo #{todo_id} to status: {status}"
    return f"Todo #{todo_id} not found"

@tool
def list_todos() -> str:
    """
    List all current todo items and their status.
    Use this to review your research plan progress.
    """
    global _todo_list
    if not _todo_list:
        return "No todos yet. Create a research plan first using create_todo."
    
    result = "Current Research Plan:\n"
    for todo in _todo_list:
        status_icon = {"pending": "⏳", "in_progress": "🔄", "completed": "✅"}.get(todo["status"], "❓")
        result += f"{status_icon} #{todo['id']} [{todo['priority']}] {todo['task']} - {todo['status']}\n"
    return result

def get_todos() -> List[Dict[str, Any]]:
    """Get the current todo list (for UI display)."""
    global _todo_list
    return _todo_list.copy()

def clear_todos():
    """Clear the todo list (for new sessions)."""
    global _todo_list
    _todo_list = []

# --- Search Tool ---

@tool
def internet_search(query: str, max_results: int = 5) -> str:
    """
    Search the internet for information.
    Before using this, make sure you have created a research plan with create_todo.
    
    Args:
        query: The search query to execute.
        max_results: Maximum number of results to return. Defaults to 5.
    """
    try:
        tavily_tool = TavilySearchResults(
            max_results=max_results,
            include_raw_content=True,
            tavily_api_key=os.getenv("TAVILY_API_KEY")
        )
        results = tavily_tool.invoke({"query": query})
        return str(results)
    except Exception as e:
        return f"Error performing search: {str(e)}"

# --- Prompts & Instructions ---

# System prompt for the research agent
SYSTEM_PROMPT = """You are a deep research assistant. Your goal is to provide comprehensive and accurate answers to user questions.

You have access to the following tools:
- create_todo: Create a research task in your plan. ALWAYS use this first!
- update_todo: Update task status to 'in_progress' or 'completed'.
- list_todos: Review your current research plan.
- internet_search: Search the web for information.

You MUST follow this exact workflow:

1. PLAN FIRST: When you receive a question, IMMEDIATELY create a todo list with 3-5 specific research tasks using create_todo. Break down the question into searchable topics.

2. EXECUTE PLAN: For each todo item:
   a. Use update_todo to mark it as 'in_progress'
   b. Use internet_search to research that specific topic
   c. Use update_todo to mark it as 'completed'

3. SYNTHESIZE: After completing all research tasks, write a comprehensive answer that:
   - Addresses all aspects of the original question
   - Cites sources from your searches
   - Provides balanced analysis

IMPORTANT: You MUST create todos BEFORE doing any searches. This is mandatory.
"""

def create_research_graph():
    """Create the deep research agent graph using LangGraph's create_react_agent."""
    llm = get_llm(temperature=0.3)
    
    # Clear todos for fresh session
    clear_todos()
    
    # All tools including todo management
    tools = [create_todo, update_todo, list_todos, internet_search]
    
    # Create the ReAct agent with system prompt
    agent = create_react_agent(
        model=llm,
        tools=tools,
        prompt=SYSTEM_PROMPT,
    )
    
    return agent
