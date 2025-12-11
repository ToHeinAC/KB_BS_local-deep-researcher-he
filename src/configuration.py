import os
from dataclasses import dataclass, fields
from typing import Any, Optional
from langchain_core.runnables import RunnableConfig

DEFAULT_REPORT_STRUCTURE = """
# Introduction
- Brief overview of the research topic or question.
- Purpose and scope of the report.

# Main Body
- Detailed explanation of concepts.
- Key findings supported by research.

# Key Takeaways
- Bullet points summarizing important insights.

# Conclusion
- Final summary and implications.
"""

@dataclass(kw_only=True)
class Configuration:
    """The configurable fields for the Deep Researcher."""
    report_structure: str = DEFAULT_REPORT_STRUCTURE
    max_search_queries: int = 5
    enable_web_search: bool = False
    enable_quality_checker: bool = True
    quality_check_loops: int = 1
    llm_model: str = "gpt-oss:20b"
    embedding_model: str = "jinaai/jina-embeddings-v2-base-de"
    selected_database: str = None
    
    def update_embedding_model(self, model_name: str) -> None:
        self.embedding_model = model_name
        
    @classmethod
    def from_runnable_config(cls, config: Optional[RunnableConfig] = None) -> "Configuration":
        configurable = (config["configurable"] if config and "configurable" in config else {})
        values: dict[str, Any] = {
            f.name: os.environ.get(f.name.upper(), configurable.get(f.name))
            for f in fields(cls)
            if f.init
        }
        return cls(**{k: v for k, v in values.items() if v})

# Global configuration instance
_config_instance = None

def get_config_instance() -> Configuration:
    global _config_instance
    if _config_instance is None:
        _config_instance = Configuration()
    return _config_instance
