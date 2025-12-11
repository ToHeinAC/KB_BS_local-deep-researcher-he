import streamlit as st
import os
import sys
import time
import json
from langchain_core.runnables.config import RunnableConfig

# Add project root to Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.state import ResearcherState, HitlState
from src.graph import create_hitl_graph, create_main_graph
from src.configuration import get_config_instance
from src.vector_db import get_embedding_model_path, get_vector_db_path, SPECIAL_DB_CONFIG
from src.rag_helpers import get_llm_models, get_license_content

# Set page config
st.set_page_config(
    page_title="Deep Researcher v0.1",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Constants
VECTOR_DB_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'kb', 'database'))

# --- Helper Functions ---

def get_available_databases():
    """Get list of available vector databases."""
    # List directories in the database folder
    dbs = []
    if os.path.exists(VECTOR_DB_DIR):
        for item in os.listdir(VECTOR_DB_DIR):
            if os.path.isdir(os.path.join(VECTOR_DB_DIR, item)):
                dbs.append(item)
    
    # Add special databases
    for key in SPECIAL_DB_CONFIG:
        if key not in dbs:
            dbs.append(key)
            
    return sorted(dbs)

def initialize_session_state():
    """Initialize session state variables."""
    if "hitl_complete" not in st.session_state:
        st.session_state.hitl_complete = False
    
    if "hitl_state" not in st.session_state:
        st.session_state.hitl_state = None
        
    if "research_state" not in st.session_state:
        st.session_state.research_state = None
        
    if "messages" not in st.session_state:
        st.session_state.messages = []
        
    if "current_phase" not in st.session_state:
        st.session_state.current_phase = "hitl" # hitl, research, complete

# --- Sidebar ---

def render_sidebar():
    with st.sidebar:
        st.title("⚙️ Configuration")
        
        config = get_config_instance()
        
        # Model Selection
        st.subheader("LLM Model")
        available_models = get_llm_models()
        
        config.llm_model = st.selectbox(
            "LLM Model", 
            available_models, 
            index=0 if available_models else None,
            help="Model used for all AI tasks (reasoning, analysis, summarization, and report writing)"
        )
        
        # Database Selection
        st.subheader("Knowledge Base")
        available_dbs = get_available_databases()
        selected_db = st.selectbox(
            "Select Vector Database",
            available_dbs,
            index=0 if available_dbs else None
        )
        if selected_db:
            config.selected_database = selected_db
            # Update embedding model based on DB name
            # Heuristic: extract model part from DB name
            # This logic should be in configuration but we do it here for UI feedback
            from src.rag_helpers import extract_embedding_model
            emb_model = extract_embedding_model(selected_db)
            config.update_embedding_model(emb_model)
            st.caption(f"Embedding Model: {emb_model}")
            
        # Research Settings
        st.subheader("Research Settings")
        config.max_search_queries = st.number_input("Max Search Queries", min_value=1, max_value=10, value=3)
        config.enable_web_search = st.checkbox("Enable Web Search", value=False)
        config.enable_quality_checker = st.checkbox("Enable Quality Checker", value=True)
        
        st.divider()
        st.markdown("### Debug Info")
        if st.checkbox("Show State"):
            if st.session_state.hitl_state:
                st.json(st.session_state.hitl_state)
            if st.session_state.research_state:
                st.json(st.session_state.research_state)

# --- HITL Phase ---

def render_hitl_phase():
    st.markdown("## 🤝 Human-in-the-Loop Research Refinement")
    
    # Initial Query Input
    if "user_query" not in st.session_state:
        query = st.chat_input("What would you like to research?")
        if query:
            st.session_state.user_query = query
            st.session_state.messages.append({"role": "user", "content": query})
            
            # Initialize HITL State
            st.session_state.hitl_state = HitlState(
                user_query=query,
                current_position=0,
                detected_language="English", # will be detected
                additional_context="",
                human_feedback="",
                analysis="",
                follow_up_questions="",
                report_llm=get_config_instance().llm_model,
                summarization_llm=get_config_instance().llm_model,
                research_queries=[],
                max_search_queries=get_config_instance().max_search_queries
            )
            
            # Run initial detection and question generation
            with st.spinner("Analyzing query and generating follow-up questions..."):
                hitl_graph = create_hitl_graph()
                # Run just the first steps
                # We need to run it step by step or invoke it
                # For simplicity, we invoke it fully but the graph structure needs to support pausing
                # Our create_hitl_graph in graph.py runs linearly to generate_knowledge_base_questions
                # This is not ideal for interactive HITL. 
                # Let's manually invoke nodes for better control here.
                
                from src.graph import detect_language, generate_follow_up_questions
                
                # 1. Detect Language
                res_lang = detect_language(st.session_state.hitl_state, None)
                st.session_state.hitl_state.update(res_lang)
                
                # 2. Generate Follow-up
                res_qs = generate_follow_up_questions(st.session_state.hitl_state, None)
                st.session_state.hitl_state.update(res_qs)
                
                # Add AI response
                ai_msg = f"I've analyzed your query. To better help you, I have a few follow-up questions:\n\n{st.session_state.hitl_state['follow_up_questions']}"
                st.session_state.messages.append({"role": "assistant", "content": ai_msg})
                st.rerun()
                
    # Chat Interface
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])
            
    # Handle subsequent feedback
    if "user_query" in st.session_state and not st.session_state.hitl_complete:
        feedback = st.chat_input("Answer the questions or provide more details (type '/end' to finish refinement)")
        if feedback:
            st.session_state.messages.append({"role": "user", "content": feedback})
            
            if feedback.strip().lower() == "/end":
                st.session_state.hitl_complete = True
                st.session_state.current_phase = "research"
                st.rerun()
            else:
                # Process feedback
                st.session_state.hitl_state["human_feedback"] = feedback
                
                with st.spinner("Analyzing feedback..."):
                    from src.graph import analyse_user_feedback, generate_follow_up_questions
                    
                    # 1. Analyze
                    res_an = analyse_user_feedback(st.session_state.hitl_state, None)
                    st.session_state.hitl_state.update(res_an)
                    
                    # 2. Generate New Follow-up
                    res_qs = generate_follow_up_questions(st.session_state.hitl_state, None)
                    st.session_state.hitl_state.update(res_qs)
                    
                    ai_msg = f"**Analysis:**\n{st.session_state.hitl_state['analysis']}\n\n**New Questions:**\n{st.session_state.hitl_state['follow_up_questions']}"
                    st.session_state.messages.append({"role": "assistant", "content": ai_msg})
                    st.rerun()

# --- Research Phase ---

def render_research_phase():
    st.markdown("## 🔬 Deep Research Execution")
    
    # If we just transitioned, generate the final research queries first
    if st.session_state.hitl_complete and not st.session_state.research_state:
        with st.status("Initializing Research Phase...", expanded=True) as status:
            st.write("Generating final research queries...")
            from src.graph import generate_knowledge_base_questions
            
            # Use current HITL state config
            config = RunnableConfig(configurable={
                "report_llm": get_config_instance().llm_model,
                "summarization_llm": get_config_instance().llm_model,
                "max_search_queries": get_config_instance().max_search_queries
            })
            
            res_kb = generate_knowledge_base_questions(st.session_state.hitl_state, config)
            st.session_state.hitl_state.update(res_kb)
            
            # Display Research Queries
            st.markdown("### 📋 Generated Research Queries")
            for i, q in enumerate(st.session_state.hitl_state["research_queries"]):
                st.markdown(f"{i+1}. {q}")
                
            # Initialize Research State
            st.session_state.research_state = ResearcherState(
                user_query=st.session_state.hitl_state["user_query"],
                detected_language=st.session_state.hitl_state["detected_language"],
                human_feedback=st.session_state.hitl_state["human_feedback"],
                additional_context=st.session_state.hitl_state["additional_context"],
                research_queries=st.session_state.hitl_state["research_queries"],
                retrieved_documents={},
                search_summaries={},
                web_search_enabled=get_config_instance().enable_web_search,
                internet_result=None,
                final_answer="",
                linked_final_answer=None,
                quality_check=None,
                reflection_count=0,
                enable_quality_checker=get_config_instance().enable_quality_checker,
                report_llm=get_config_instance().llm_model,
                summarization_llm=get_config_instance().llm_model,
                selected_database=get_config_instance().selected_database
            )
            
            status.update(label="Research Phase Initialized", state="complete", expanded=False)
            
    # Execute Main Graph
    if st.button("🚀 Start Deep Research", type="primary"):
        research_placeholder = st.empty()
        main_graph = create_main_graph()
        
        with st.status("Executing Research Workflow...", expanded=True) as status:
            
            # Stream events
            st.session_state.research_state["final_answer"] = "" # Reset
            
            final_state = None
            for event in main_graph.stream(st.session_state.research_state):
                for key, value in event.items():
                    st.write(f"Completed step: **{key}**")
                    if key == "retrieve_rag_documents":
                        with st.expander("📄 Retrieved Documents", expanded=False):
                            st.json(value.get("retrieved_documents", {}))
                    elif key == "summarize_query_research":
                        with st.expander("📝 Summaries", expanded=False):
                            # value is state update, search_summaries might be in it or in final state
                            if "search_summaries" in value:
                                st.write(f"Generated summaries for {len(value['search_summaries'])} queries")
                    elif key == "web_search":
                        with st.expander("🌐 Web Search Results", expanded=False):
                            st.write(value.get("internet_result", "No results"))
                    elif key == "quality_checker":
                        with st.expander("✅ Quality Check", expanded=True):
                            qc = value.get("quality_check", {})
                            st.write(f"Score: {qc.get('quality_score', 'N/A')}")
                            st.write(f"Accurate: {qc.get('is_accurate', 'N/A')}")
                            if not qc.get('is_accurate', False):
                                st.write(f"Issues: {qc.get('issues_found', '')}")
                                st.info("Reflecting and regenerating...")
                    elif key == "generate_final_answer":
                        # Interim answer
                        pass
                    
                    # Update session state with progress
                    if st.session_state.research_state and value:
                        st.session_state.research_state.update(value)
                    final_state = st.session_state.research_state
            
            status.update(label="Research Complete", state="complete", expanded=False)
            st.session_state.current_phase = "complete"
            st.rerun()

# --- Completion Phase ---

def render_completion_phase():
    st.markdown("## 🎯 Final Report")
    
    if st.session_state.research_state and st.session_state.research_state.get("final_answer"):
        final_answer = st.session_state.research_state.get("linked_final_answer") or st.session_state.research_state.get("final_answer")
        
        # Display thinking if available
        from src.utils import parse_output
        parsed = parse_output(final_answer)
        
        if parsed["reasoning"]:
            with st.expander("🧠 Thinking Process"):
                st.markdown(parsed["reasoning"])
                
        st.markdown(parsed["response"], unsafe_allow_html=True)
        
        st.divider()
        col1, col2 = st.columns(2)
        with col1:
            st.download_button(
                "📥 Download Report",
                data=parsed["response"],
                file_name="research_report.md",
                mime="text/markdown"
            )
        with col2:
            if st.button("🔄 New Research"):
                st.session_state.clear()
                st.rerun()
    else:
        st.error("No final answer generated.")

# --- Main App ---

def main():
    initialize_session_state()
    render_sidebar()
    
    # Add header image if it exists
    header_image_path = os.path.join(os.path.dirname(__file__), '..', 'Header für Chatbot.png')
    if os.path.exists(header_image_path):
        st.image(header_image_path, use_column_width=True)
    
    st.title("🔍 Local Deep Researcher")
    st.caption("Agentic RAG with Human-in-the-Loop")
    
    if st.session_state.current_phase == "hitl":
        render_hitl_phase()
    elif st.session_state.current_phase == "research":
        render_research_phase()
    elif st.session_state.current_phase == "complete":
        render_completion_phase()

if __name__ == "__main__":
    main()
