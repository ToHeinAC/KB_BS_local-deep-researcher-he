# KB_BS_local-deep-researcher-he_v0.1_SPEC.md
Software Requirements Specification (SRS)

## Scope & goals:
The scope is tho build a fully locally runnable deep researcher using langchain deep agents framework. The functionalities shall be close to those in https://github.com/ToHeinAC/KB_BS_local-rag-he and there app_v2_1g.py. This means essentially that the deep researcher must be able to connect to a local vector database and be able to do agentic research based on an initial user query which is concretized by an initial human-in-the-loop (HITL) process. This initial HITL process must be able to understand the humans query and make deep questions by the deep researcher to be answered by the human in order to get a better understanding of the topic, i.e. an optimized context, to be more precise in the search for information. 

### In scope:
- Deep researcher 
- fully local implementation including local vector database and local LLMs
- stand-alone-repo (no imports from other users repos)
- main functionalities as in https://github.com/ToHeinAC/KB_BS_local-rag-he and there app_v2_1g.py (e.g. HITL, vector database search, summarization, nternet search (optional), quality assurance,final report generation) 
- nice streamlit app web interface 
- web app configuration (LLM, vector database, results per vector database search, etc.; see https://github.com/ToHeinAC/KB_BS_local-rag-he and there app_v2_1g.py)
- display of all relevant preliminary results (see https://github.com/ToHeinAC/KB_BS_local-rag-he and there app_v2_1g.py)
### Out of scope (for now):
- long term memory
- user profile and logins
- session management
- vector database generation, management etc. (this is done elsewhere for now)

## User stories:
- As the end-user I want to have a GUI for a good user experience tho work with the deep researcher in order to deploy the solution in the end to less technically experienced users. 
- As the end-user, In the GUI, I want to choose from a local LLMs (e.g. gpt-oss:20b from ollama, mistralai/Ministral-3-14B-Reasoning-2512 from huggingface) in the GUI in order to be able to get different results for the same initial query since each LLM has its own style and approach
- As the end-user, In the GUI, I want to choose the vector database in order to be able to make deep research on a dedicated set of information. The vector database must be already there.
- As the end-user, In the GUI, I want to be able to set important parameters such as the numbers of retrieved results from the vector database for each query.
- As the end-user, In the GUI, I want to have a simple but nice looking window to type the prompt (similar to chatgpt).
- As the end-user, In the GUI, In the HITL phase, I want to be able to see the context from the original query and all the analysis from the researcher after the answers of the questions from the human-in-the-loop. 
- As the end-user, In the GUI, I must be able to end the HITL phase such that the next steps of the deep researcher are executed.
- As the end-user, In the GUI, I want to be able to see the final report generation as well as all relevant preliminary results. Use expanders wherever useful. This shall help to get good insights into the final answer generation as a possibility for human quality assurance.
- As the end-user, In the GUI, I want to be able to see the current researcher step and the previous step to be able to get a good sense of what is happening behind the scenes.  
- As the end-user, In the GUI, I want to be able to see the references for the final result. These shall be clickable links to the original sources.  
- As the end-user, In the GUI, I want to be able to activate web seach (default: No web seach) and source linking in the final answer(default: No source linking).
- As the end user, I am critically dependend on the deep reserchers honesty in the sense that in case the initiel query and the subsequent HITL interaction is on another topic as the chosen vector database, the deep researcher must be able to detect this and stop the deep researcher process as well as state that the query cannot be answered based on the chosen vector database. E.g. for the end-user it must be clear that in case the initial query and HITL phase is on topic quantum mechanics and the vector database is on topic formula one racing, the deep researcher must be able to detect this at a certain point and stop the deep researcher process as well as state that the query cannot be answered based on the chosen vector database.
- As the software architect, behind the scenes, I want the deep researcher to be able to verify the most important steps in the workflow (i.e. reflection) in order to guarantee the highest quality of the final answer generation. Moreover, reflections shall be used to check if the quality of the answer has a good level.
- As the software architect, behind the scenes, I want the deep researcher to be able stop the deep research loops after a maximum number of attempts in order to prevent infinite loops. When this happens, this must be displayed in the GUI in order to let the end-user know if there could be a quality issue in case the maximum number of attemps was reached.
- As the software architect, behind the scenes, I want the deep researcher to store a meanigful set of debugging information into a file "debugging_info.txt" in the dev folder in order to be able to debug the deep researcher in case of issues.
## Functional requirements:
- An stremalit application file taking into account all the GUI-specific user stories
- Helper functions for the deep researcher state, the prompts and the tools
- At least 4 tools for the deep researcher: a vector database retriever, a web search tool, a quality checker tool, a final report generator tool
- Summarization shall be a required step after each vector database retrieval. 
- In th GUI there must be a checkbox for optional web seach and source linking. When activated, web search shall be a required step after vector database retrieval is finished and source linking shall be a required step after final report generation is finished.   

## Non‑functional requirements:
Use the following hierarchy for your files to be generated
- The streamlit app ("app_v0_1g.py" for now)must be in the apps folder
- The helper functions which are imported in the streamlit app must be in the src folder. Use different files at least for the deep researchers state, the prompts and the tools
- The debug info must be stored to "debugging_info.txt" in the dev folder
- The .gitignore file must be such that the kb folder is excluded from version control

### Important main resources

- https://github.com/langchain-ai/deepagents
- https://docs.langchain.com/oss/python/deepagents/overview
- https://blog.langchain.com/deep-agents/
- https://www.youtube.com/watch?v=yTWocbVKQxw

### Important subresources

- https://www.youtube.com/watch?v=TTMYJAw5tiA
- https://www.youtube.com/watch?v=AZ6257Ya_70
- https://github.com/langchain-ai/deep-agents-ui
- https://www.youtube.com/watch?v=IVts6ztrkFg
- https://www.youtube.com/watch?v=39mZvpN0k-Q
- https://www.youtube.com/watch?v=5tn6O0uXYEg
- https://www.youtube.com/watch?v=SpfT6-YAVPk
- https://www.youtube.com/watch?v=A1t53E4vtGo

### tech constraints:
- The LLM must be fully local, use gpt-oss:20b from ollama (already locally installed/available); additionally the implementation must be robust such that mistralai/Ministral-3-14B-Reasoning-2512 from huggingface can be used as an second option 
- You must implement the researcher strictly using langchains deep agents framework https://docs.langchain.com/oss/python/deepagents/overview#deep-agents-overview. Make use at least of the core capabilities "Planning and task decomposition", "Context management" and "Subagent spawning", that is use the Deep Agents Middleware architecture
- Use uv for virtual environment management and running the researcher
- make sure that version control is used (github/ToHeinAC/KB_BS_local-deep-researcher-he)
- make sure that a nice app for runnig is there (must be streamlit, see https://github.com/ToHeinAC/KB_BS_local-rag-he and there app_v2_1g.py); the port should be 8508
## Success criteria: 
- Each implementation step is well tested
- Each implementation step is well documented (different README files for different steps)
- The tech constraints are fulfilled
- The core capabilities of the deep agents framework as stated in the tech constraints are used
- The functional requirements are fulfilled
- The non-functional requirements are fulfilled

