
import sys
import os
import json
from langchain_core.messages import HumanMessage
from langchain_ollama import ChatOllama

# Add the showroom directory to path
sys.path.append(os.path.abspath("showroom"))

try:
    from deepagents.middleware.subagents import _create_task_tool
    from langchain_core.tools import tool
    
    # Create a dummy subagent graph (needs to be a compiled graph or runnable)
    # We can just use a dummy callable or object that looks like a graph
    class MockGraph:
        def invoke(self, *args, **kwargs):
            return {"messages": []}
            
    mock_graph = MockGraph()
    
    # create task tool
    # Signature: _create_task_tool(name: str, description: str, subagent_graph: Any) -> BaseTool
    print("Creating task tool...")
    task_tool = _create_task_tool(
        name="research_agent",
        description="Description of research agent",
        subagent_graph=mock_graph
    )
    
    print(f"Tool created: {task_tool.name}")
    print(f"Args schema: {task_tool.args_schema.schema_json(indent=2)}")
    
    # Now try to bind this to Ollama
    print("\nBinding to Ollama...")
    llm = ChatOllama(model="gpt-oss:20b", temperature=0)
    llm_with_tools = llm.bind_tools([task_tool])
    
    print("Invoking...")
    # We don't need to actually run the tool, just see if Ollama accepts the schema
    # But the error happens during generation/execution of template on Ollama side, so invoke is needed.
    response = llm_with_tools.invoke("Use the research_agent to find out about bitcoin.")
    print("Success!")
    print(response)

except Exception as e:
    print(f"\nError occurred: {e}")
    # import traceback
    # traceback.print_exc()
