# Deep Researcher Implementation

This folder contains the implementation of the Local Deep Researcher using LangChain Deep Agents.

## Overview

The solution implements a Deep Researcher agent capable of performing deep research tasks using a local LLM (`gpt-oss:20b`) and Internet Search (Tavily). It uses the **Deep Agents** framework to manage planning, sub-agents, and a virtual file system.

## Components

### 1. Backend (`backend.py`)
- **Main Agent**: Orchestrates the research process, manages the plan, and coordinates sub-agents.
- **Sub-agents**:
  - **Research Agent**: Conducts focused research on specific sub-topics using internet search.
  - **Critique Agent**: Reviews the final report for accuracy, completeness, and structure.
- **Tools**:
  - **Internet Search**: Uses Tavily API to search the web (requires `TAVILY_API_KEY`).
- **LLM**: configured to use `gpt-oss:20b` via Ollama.

### 2. Frontend (`app.py`)
- **Streamlit Interface**: A modern, chat-based UI.
- **Features**:
  - Chat interface for interacting with the researcher.
  - Real-time status updates showing tool usage and sub-agent activities.
  - **Plan & To-Dos**: Visualizes the agent's current plan and progress.
  - **Virtual File System**: Displays files created by the agent (e.g., `final_report.md`, `question.txt`).

## Setup & Running

1. **Prerequisites**:
   - Python >= 3.11
   - `uv` package manager
   - Ollama running with `gpt-oss:20b` (or `deepseek-r1:latest` as fallback)
   - Tavily API Key

2. **Installation**:
   ```bash
   uv sync
   ```

3. **Environment Variables**:
   Create a `.env` file in the root or `showroom/` directory:
   ```env
   TAVILY_API_KEY=tvly-...
   ```

4. **Running the App**:
   ```bash
   uv run streamlit run showroom/app.py --server.port 8508 --server.headless false
   ```

## Architecture

The implementation follows the [Deep Agents Deep Research](https://github.com/langchain-ai/deepagents-quickstarts/tree/main/deep_research) pattern:

1.  **Plan**: The agent breaks down the user query into tasks (To-Dos).
2.  **Act**: It delegates research tasks to the **Research Agent**.
3.  **Synthesize**: Findings are compiled into a report.
4.  **Critique**: The **Critique Agent** reviews the report.
5.  **Refine**: The agent improves the report based on feedback.
6.  **Deliver**: The final answer is presented to the user.

## Dependencies

- `deepagents`: Core agent framework.
- `langchain-ollama`: Local LLM integration.
- `tavily-python`: Web search.
- `streamlit`: User interface.
