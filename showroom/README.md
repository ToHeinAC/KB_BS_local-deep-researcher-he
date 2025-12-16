# Local Deep Researcher (Showroom)

This directory contains the initial implementation of the Local Deep Researcher, built using the **LangChain Deep Agents** framework. It is designed to run locally using Ollama for LLM inference and Tavily for internet search.

## Solution Overview

The Local Deep Researcher is an intelligent agent capable of performing deep research tasks. It breaks down complex user queries, spawns sub-agents to research specific topics, verifies findings, and synthesizes a comprehensive final report.

### Key Features
*   **Fully Local LLM**: Uses `gpt-oss:20b` (via Ollama) for all reasoning and generation tasks.
*   **Deep Agents Framework**: Leverages LangChain's `deepagents` for hierarchical planning, sub-agent coordination, and context management.
*   **Internet Search**: Integrates Tavily Search API for retrieving real-time information.
*   **Virtual File System**: Agents interact with a virtual file system to store notes, drafts, and the final report (`final_report.md`).
*   **Streamlit GUI**: A modern, chat-based interface that visualizes the agent's thought process, active plans (To-Dos), and created files.

## Architecture

The system consists of:
1.  **Main Agent**: The orchestrator that interacts with the user, creates plans, and delegates tasks.
2.  **Research Sub-Agent**: A specialized agent dedicated to deep-diving into specific sub-topics using web search.
3.  **Critique Sub-Agent**: A quality control agent that reviews the final report for accuracy, structure, and completeness before presentation.

## Prerequisites

Before running the application, ensure you have the following:

1.  **Python >= 3.11**
2.  **uv** (Python package manager)
3.  **Ollama** running locally with the required model:
    ```bash
    ollama pull gpt-oss:20b
    ```
    *(Note: You can fallback to `deepseek-r1:latest` by editing `backend.py` if needed)*
4.  **Tavily API Key**: Get one at [tavily.com](https://tavily.com).

## Setup

1.  **Install Dependencies**:
    Navigate to the project root and run:
    ```bash
    uv sync
    ```

2.  **Configure Environment**:
    Create a `.env` file in the project root (or ensure it exists):
    ```env
    TAVILY_API_KEY=tvly-your-api-key-here
    ```

## Launching the Application

To start the Deep Researcher interface, run the following command from the project root:

```bash
uv run streamlit run showroom/app.py --server.port 8508 --server.headless false
```

Once running, the application will be accessible at `http://localhost:8508`.

## Usage

1.  Enter your research topic in the chat input (e.g., "What is the current state of solid-state battery technology?").
2.  Observe the **Plan & To-Dos** in the sidebar as the agent decomposes the task.
3.  Watch the **Status** updates in the chat to see real-time tool usage and sub-agent activity.
4.  Review generated files (like `final_report.md`) in the **Virtual File System** section of the sidebar.
