
import sys
import os
from langchain_ollama import ChatOllama
from deepagents import create_deep_agent
from langchain_core.messages import HumanMessage
from langchain_community.tools.tavily_search import TavilySearchResults
from dotenv import load_dotenv

# Add showroom to path
sys.path.append(os.path.abspath("showroom"))
load_dotenv()

# Setup same as backend.py but NO SUBAGENTS
llm = ChatOllama(model="gpt-oss:20b", temperature=0)

tavily = TavilySearchResults(max_results=3)

try:
    print("Creating agent WITHOUT subagents...")
    agent = create_deep_agent(
        model=llm,
        tools=[tavily],
        system_prompt="You are a helper.",
        # subagents=[] # EXPLICITLY EMPTY
    )
    
    print("Invoking agent...")
    inputs = {"messages": [HumanMessage(content="What is the weather in SF?")]}
    for event in agent.stream(inputs, stream_mode="values"):
        if "messages" in event:
            last = event["messages"][-1]
            print(f"Msg: {type(last)}")
            if hasattr(last, "content"):
                print(f"Content: {last.content[:50]}...")

    print("Success without subagents.")

except Exception as e:
    print(f"Error without subagents: {e}")
