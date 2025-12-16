
import sys
import os
import json
from langchain_core.messages import HumanMessage
from langchain_core.tools import tool

# Add the showroom directory to path
sys.path.append(os.path.abspath("showroom"))

import backend

try:
    print("Creating research graph...")
    graph = backend.create_research_graph()
    
    # The graph is a CompiledStateGraph. We want to see what tools are bound to the model.
    # Usually deepagents creates a graph where the 'agent' node calls the model.
    # Getting the model with bound tools from the graph object is not straightforward without running it,
    # or inspecting the internal nodes.
    
    # However, create_deep_agent returns a CompiledGraph.
    # Let's try to inspect the 'agent' node if possible, or we can try to "mock" the deep agent creation 
    # and print tools before binding.
    
    # Alternatively, we can look at what `create_deep_agent` does. 
    # It adds tools. Let's try to replicate the tool creation part.
    
    # Let's inspect the graph nodes
    print("Graph nodes:", graph.nodes.keys())
    
    # If we can't easily inspect the bound model, we can try to call create_deep_agent 
    # with a mock model wrapper that intercepts the bind_tools call?
    
    from deepagents import create_deep_agent
    from langchain_ollama import ChatOllama
    
    class MockModel(ChatOllama):
        def bind_tools(self, tools, **kwargs):
            print(f"Binding {len(tools)} tools:")
            for t in tools:
                print(f" - {t.name}: {t.description}")
                try:
                    # Print schema to see if anything looks weird
                    if hasattr(t, 'args_schema') and t.args_schema:
                         print(f"   Schema: {t.args_schema.schema_json()}")
                except Exception as e:
                    print(f"   Error printing schema: {e}")
            return super().bind_tools(tools, **kwargs)

    llm = MockModel(model="gpt-oss:20b", temperature=0)
    
    # Recreate config from backend.py
    RESEARCH_AGENT_PROMPT = "Research prompt"
    internet_search = backend.internet_search
    
    research_agent_config = {
        "name": "research_agent",
        "description": "Use to research.",
        "system_prompt": RESEARCH_AGENT_PROMPT,
        "tools": [internet_search],
    }
    
    # Create agent with mock model to see tools
    print("\n--- Creating Deep Agent with Mock Model ---")
    create_deep_agent(
        model=llm,
        tools=[internet_search],
        system_prompt="Main prompt",
        subagents=[research_agent_config],
    )

except Exception as e:
    print(f"\nError occurred: {e}")
    import traceback
    traceback.print_exc()
