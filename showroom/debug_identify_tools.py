
import sys
import os
from langchain_ollama import ChatOllama
from deepagents.tools.files import FileSystemTools
from deepagents.tools.todos import TodoTools
# Note: Import paths are guesses based on common patterns, if they fail I will list dir of deepagents package

def test_tool_binding(tools, name):
    print(f"Testing binding for {name}...")
    try:
        llm = ChatOllama(model="gpt-oss:20b", temperature=0)
        llm_with_tools = llm.bind_tools(tools)
        # We need to invoke to trigger the error on Ollama side
        llm_with_tools.invoke("test")
        print(f"✅ {name} works.")
    except Exception as e:
        print(f"❌ {name} FAILED: {e}")

try:
    # Try to import and inspect deepagents tools
    # If imports fail, we will use inspect module on the package
    import deepagents
    print(f"Deepagents path: {deepagents.__path__}")
    
    # Based on typical agent frameworks, look for tools
    # We can also try to create an agent and access .tools from it if possible, 
    # but the graph hides it. 
    # Let's try to access typical tool modules.
    
except Exception as e:
    print(e)
