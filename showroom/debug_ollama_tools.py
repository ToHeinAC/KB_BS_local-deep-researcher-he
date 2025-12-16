
import os
from dotenv import load_dotenv
from langchain_ollama import ChatOllama
from langchain_core.tools import tool
from langchain_core.messages import HumanMessage

load_dotenv()

# Define the tool as in backend.py
@tool
def internet_search(query: str, max_results: int = 5, include_raw_content: bool = True) -> str:
    """
    Search the internet for information.
    
    Args:
        query: The search query to execute.
        max_results: Maximum number of results to return. Defaults to 5.
        include_raw_content: Whether to include raw content in results. Defaults to True.
    """
    return "Mock search result"

# Configuration
LLM_MODEL = "gpt-oss:20b"

print(f"Testing model: {LLM_MODEL}")

try:
    llm = ChatOllama(model=LLM_MODEL, temperature=0)
    
    # Bind tools
    llm_with_tools = llm.bind_tools([internet_search])
    
    # Invoke
    print("Invoking LLM with tools...")
    response = llm_with_tools.invoke([HumanMessage(content="Why is bitcoin down?")])
    print("Response received:")
    print(response)

except Exception as e:
    print(f"\nError occurred: {e}")
