import streamlit as st
import os
import asyncio
from dotenv import load_dotenv
from backend import create_research_graph, get_todos, clear_todos
from langchain_core.messages import HumanMessage, AIMessage, ToolMessage

# Load environment variables
load_dotenv()

# Page configuration
st.set_page_config(
    page_title="Deep Researcher",
    page_icon="🕵️‍♂️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .stChatInput {
        position: fixed;
        bottom: 0;
        padding-bottom: 20px;
    }
    .report-container {
        border: 1px solid #ddd;
        padding: 20px;
        border-radius: 10px;
        background-color: #f9f9f9;
        margin-top: 20px;
    }
    .todo-item {
        padding: 5px 10px;
        margin: 5px 0;
        background-color: #eef;
        border-radius: 5px;
        border-left: 3px solid #00f;
    }
    .file-item {
        font-family: monospace;
        padding: 5px;
        border-bottom: 1px solid #eee;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []
if "graph" not in st.session_state:
    st.session_state.graph = create_research_graph()
if "files" not in st.session_state:
    st.session_state.files = {}
if "todos" not in st.session_state:
    st.session_state.todos = []

# Sidebar
with st.sidebar:
    st.title("🕵️‍♂️ Deep Researcher")
    st.markdown("Powered by **LangGraph ReAct Agent** & **Ollama**")
    
    st.divider()
    
    # Status & Todos - fetch from backend
    st.subheader("📋 Research Plan")
    todos = get_todos()
    if todos:
        for todo in todos:
            status_icon = {"pending": "⏳", "in_progress": "🔄", "completed": "✅"}.get(todo["status"], "❓")
            priority_color = {"high": "#ff6b6b", "medium": "#4dabf7", "low": "#69db7c"}.get(todo["priority"], "#868e96")
            st.markdown(f"""
                <div class='todo-item' style='border-left-color: {priority_color};'>
                    {status_icon} <strong>#{todo['id']}</strong> {todo['task']}
                    <br><small style='color: gray;'>{todo['priority']} priority • {todo['status']}</small>
                </div>
            """, unsafe_allow_html=True)
    else:
        st.info("No research plan yet. Ask a question to start!")
    
    # New research button
    if st.button("🔄 New Research", use_container_width=True):
        clear_todos()
        st.session_state.messages = []
        st.session_state.graph = create_research_graph()
        st.rerun()
        
    st.divider()
    
    # File System
    st.subheader("📂 Virtual File System")
    if st.session_state.files:
        for filename, content in st.session_state.files.items():
            with st.expander(f"📄 {filename}"):
                st.code(content)
    else:
        st.info("No files created yet.")

# Main Chat Interface
st.title("Deep Research Assistant")

# Display chat history
for msg in st.session_state.messages:
    if isinstance(msg, HumanMessage):
        with st.chat_message("user"):
            st.markdown(msg.content)
    elif isinstance(msg, AIMessage):
        with st.chat_message("assistant"):
            st.markdown(msg.content)
    # Tool messages are generally hidden or shown in expanders, 
    # for cleaner UI we skip them in main chat or show as status updates during streaming

# Chat input
if prompt := st.chat_input("What would you like to research?"):
    # Add user message to state
    user_msg = HumanMessage(content=prompt)
    st.session_state.messages.append(user_msg)
    with st.chat_message("user"):
        st.markdown(prompt)

    # Process with Agent
    with st.chat_message("assistant"):
        status_container = st.status("Thinking & Researching...", expanded=True)
        
        try:
            # Prepare inputs - deeper agents might expect different input formats, 
            # but usually it's a list of messages or a dictionary.
            inputs = {"messages": st.session_state.messages}
            
            # Streaming execution
            full_response = ""
            final_messages = []
            
            # Stream through all events
            for event in st.session_state.graph.stream(inputs, stream_mode="values"):
                if "messages" in event and event["messages"]:
                    final_messages = event["messages"]
                    last_msg = event["messages"][-1]
                    
                    if isinstance(last_msg, AIMessage):
                        # Show tool calls in status
                        if last_msg.tool_calls:
                            for tool_call in last_msg.tool_calls:
                                tool_name = tool_call['name']
                                if tool_name == 'create_todo':
                                    task = tool_call['args'].get('task', '')
                                    status_container.write(f"📝 Planning: **{task}**")
                                elif tool_name == 'update_todo':
                                    status_container.write(f"📋 Updating task status...")
                                elif tool_name == 'list_todos':
                                    status_container.write(f"📋 Reviewing plan...")
                                elif tool_name == 'internet_search':
                                    query = tool_call['args'].get('query', '')
                                    status_container.write(f"🔍 Searching: **{query}**")
                        # Capture AI content for final display
                        if last_msg.content:
                            full_response = last_msg.content
                                
                    elif isinstance(last_msg, ToolMessage):
                        # Don't spam "Found information" for every tool
                        pass

            # Update session state with final messages
            st.session_state.messages = final_messages
            status_container.update(label="Research Complete", state="complete", expanded=False)
            
            # Display the final response AFTER the status container
            if full_response:
                st.markdown(full_response)
            
        except Exception as e:
            st.error(f"An error occurred: {str(e)}")
            status_container.update(label="Error", state="error")

