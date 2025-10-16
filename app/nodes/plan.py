from typing import Any, Dict, List
from ..util.types import AgentState

def node_plan(state: AgentState) -> AgentState:
    # 각 의도(intent)에 따른 계획(plan) 수립
    steps: List[Dict[str, Any]] = []
    if state.needs_rag:
        steps.append({"op": "rag.retrieve", "top_k": 10, "filters": {"team": "*"}})
    if state.intent == "jira":
        steps.append({"op": "jira.query", "jql": None})
    if state.intent == "metrics":
        steps.append({"op": "prom.query", "promql": None, "range": ["-1h", "now"], "step": 30})
    if state.intent == "docs":
        steps.append({"op": "conf.search", "query": None})
    steps.append({"op": "synthesize"})
    state.plan_steps = steps
    state.events.append(f"plan:steps={steps}")
    return state