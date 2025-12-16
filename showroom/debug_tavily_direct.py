
import os
from dotenv import load_dotenv
from langchain_ollama import ChatOllama
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_core.messages import HumanMessage

load_dotenv()

llm = ChatOllama(model="gpt-oss:20b", temperature=0)
tavily = TavilySearchResults(max_results=3)

try:
    print("Binding TavilySearchResults to ChatOllama...")
    llm_with_tools = llm.bind_tools([tavily])
    
    print("Invoking...")
    response = llm_with_tools.invoke([HumanMessage(content="Search for python news")])
    print("Success!")
    print(response)

except Exception as e:
    print(f"Error with Tavily direct bind: {e}")
