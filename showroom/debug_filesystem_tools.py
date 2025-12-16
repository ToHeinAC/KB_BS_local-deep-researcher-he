
import sys
import os
from langchain_ollama import ChatOllama
from deepagents.middleware.filesystem import FilesystemMiddleware

# Add showroom to path
sys.path.append(os.path.abspath("showroom"))

try:
    print("Initializing FileSystemMiddleware...")
    # Middleware usually adds tools to the agent or context
    # Let's see if we can get the tools directly.
    # Looking at directory listing, there is no separate 'tools' package exposed easily in top level list
    # but middleware/filesystem.py likely contains the tool definitions or classes.
    
    # Let's try to instantiate the middleware and see if it exposes tools
    fs = FilesystemMiddleware()
    
    # Inspect if it has tools
    tools = []
    if hasattr(fs, 'tools'):
        tools = fs.tools
    elif hasattr(fs, 'get_tools'):
        tools = fs.get_tools()
        
    print(f"Found {len(tools)} tools in FileSystemMiddleware")
    
    if tools:
        print("Binding FileSystem tools to Ollama...")
        llm = ChatOllama(model="gpt-oss:20b", temperature=0)
        llm_with_tools = llm.bind_tools(tools)
        
        print("Invoking...")
        llm_with_tools.invoke("List files")
        print("✅ FileSystem tools work.")
    else:
        print("No tools found to test.")

except Exception as e:
    print(f"❌ FileSystem tools FAILED: {e}")
