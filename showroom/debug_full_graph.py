
import sys
import os
from langchain_core.messages import HumanMessage

# Add the showroom directory to path
sys.path.append(os.path.abspath("showroom"))

try:
    import backend
    print("Creating research graph...")
    graph = backend.create_research_graph()
    
    query = "Why is bitcoin down?"
    print(f"Invoking graph with query: {query}")
    
    inputs = {"messages": [HumanMessage(content=query)]}
    
    for event in graph.stream(inputs, stream_mode="values"):
        if "messages" in event:
            last_msg = event["messages"][-1]
            print(f"Last message type: {type(last_msg)}")
            if hasattr(last_msg, "content"):
                print(f"Content: {last_msg.content[:100]}...")
            if hasattr(last_msg, "tool_calls") and last_msg.tool_calls:
                print(f"Tool calls: {last_msg.tool_calls}")

except Exception as e:
    print(f"\nError occurred: {e}")
    import traceback
    traceback.print_exc()
