import os
DB_PATH = os.getenv("CHECKPOINT_DB", "state.db")
LLM_API_KEY = os.getenv("LLM_KEY", "demo")
LLM_BASE_URL = os.getenv("LLM_BASE_URL", "https://llm.local")
JIRA_BASE = os.getenv("JIRA_BASE", "https://jira.local")
CONF_BASE = os.getenv("CONF_BASE", "https://conf.local")
PROM_BASE = os.getenv("PROM_BASE", "https://prom.local")
VECTORDB_URL = os.getenv("VECTORDB_URL", "qdrant://localhost:6333")
MAX_HARD_TOKENS = 64000
SOFT_BUDGET = int(MAX_HARD_TOKENS * 0.75)