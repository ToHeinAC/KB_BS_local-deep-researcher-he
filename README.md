# KB_BS_local-deep-researcher-he

A fully local Deep Researcher application using LangChain, LangGraph, and Ollama.

## Features

- **Human-in-the-Loop (HITL)**: Interactive refinement of research queries before execution.
- **Deep Research Agent**: Autonomous multi-step research process:
    - Language Detection
    - Query Expansion (Knowledge Base Questions)
    - Retrieval Augmented Generation (RAG) from local Vector DB
    - Document Summarization
    - Summary Reranking
    - Web Search (Optional, via Tavily)
    - Final Report Generation
    - Quality Assurance Loop
- **Local Privacy**: Runs with local LLMs (Ollama) and local Vector Database.
- **Streamlit UI**: User-friendly interface for configuration and interaction.

## Prerequisites

- Python 3.10+
- [Ollama](https://ollama.com/) running locally with models:
    - `deepseek-r1:latest` (or `gpt-oss:20b`)
    - `llama3.2:latest` (for summarization)
- Local Vector Database (compatible with Chroma/HuggingFace embeddings)

## Installation

1. Clone the repository (if not already done).
2. Install dependencies using `uv` or `pip`:

```bash
# Using uv (Recommended)
uv pip install -r requirements.txt
# OR install via pyproject.toml
uv pip install .
```

## Configuration

The application uses environment variables and UI settings. 
Create a `.env` file in the root if necessary, or configure via the Sidebar.

Key settings:
- `LLM_MODEL`: Default LLM model
- `REPORT_LLM`: Model for report generation
- `TAVILY_API_KEY`: For optional web search

## Usage

Run the Streamlit app:

```bash
streamlit run apps/app_v0_1g.py --server.port 8508
```

## Structure

- `apps/`: Streamlit application files.
- `src/`: Core logic (Graph, State, Tools, Utils).
- `kb/`: Knowledge base directory (for vector db).
- `docs/`: Documentation.

## License

Apache 2.0
