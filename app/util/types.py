from __future__ import annotations
from typing import Optional, List, Dict, Any, Literal
from pydantic import BaseModel, Field

Intent = Literal["jira", "docs", "metrics", "general", "law"]

class AgentState(BaseModel):
    # Inputs
    user_id: str
    session_id: str
    user_query: str

    # Routing / planning
    intent: Optional[Intent] = None
    intent_conf: float = 0.0
    needs_rag: bool = False
    plan_steps: List[Dict[str, Any]] = Field(default_factory=list)

    # Tool IO buffers
    rag_results: List[Dict[str, Any]] = Field(default_factory=list)
    jira_results: List[Dict[str, Any]] = Field(default_factory=list)
    conf_results: List[Dict[str, Any]] = Field(default_factory=list)
    prom_results: Optional[Dict[str, Any]] = None

    # Final assembly
    answer_draft: str = ""
    answer_final: str = ""
    citations: List[Dict[str, Any]] = Field(default_factory=list)
    confidence: float = 0.0
    done: bool = False

    # Context management
    stm_summary: List[str] = Field(default_factory=list)
    ltm_keys: List[str] = Field(default_factory=list)

    # Control / runtime
    cancel_token: Optional[str] = None
    events: List[str] = Field(default_factory=list)