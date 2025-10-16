from ..util.types import AgentState
from ..services.mcp_confluence import ConfluenceMCP
from ..services.mcp_prometheus import PrometheusMCP
from ..services.vectordb import VectorDB
from ..util.context import assemble_context

class Services:
    def __init__(self, llm_small: LLMClient, llm_large: LLMClient, jira: JiraMCP, conf: ConfluenceMCP, prom: PrometheusMCP, vectordb: VectorDB):
        self.llm_small = llm_small
        self.llm_large = llm_large
        self.jira = jira
        self.conf = conf
        self.prom = prom
        self.vectordb = vectordb


def node_act(state: AgentState, svc: Services) -> AgentState:
    for step in state.plan_steps:
        if state.cancel_token:
            state.events.append("act:cancelled")
            break
        op = step.get("op")
        if op == "rag.retrieve":
            state.rag_results = svc.vectordb.retrieve(state.user_query, top_k=step.get("top_k", 10), filters=step.get("filters"))
            state.events.append(f"rag:retrieved={len(state.rag_results)}")
        elif op == "jira.query":
            jql = step.get("jql")
            if not jql:
                jql_prompt = [
                    {"role": "system", "content": "Make a minimal JQL for the user query."},
                    {"role": "user", "content": state.user_query}
                ]
                jql = svc.llm_small.call(model="32B", messages=jql_prompt)
                jql = f"project = DEMO AND text ~ '{state.user_query[:40]}'" # sanitize placeholder
            rows = svc.jira.search(jql, limit=10)
            state.jira_results = rows
            state.citations.extend({"type": "jira", "url": r["url"]} for r in rows)
            state.events.append(f"jira:rows={len(rows)}")
        elif op == "prom.query":
            promql = step.get("promql") or "rate(http_requests_total[1m])"
            import time
            end = int(time.time()); start = end - 3600
            res = svc.prom.query_range(promql, start=start, end=end, step=step.get("step", 30))
            state.prom_results = res
            state.events.append("prom:queried")
        elif op == "conf.search":
            q = step.get("query") or state.user_query
            rows = svc.conf.search(q, limit=5)
            state.conf_results = rows
            state.citations.extend({"type": "conf", "url": r["url"]} for r in rows)
            state.events.append(f"conf:rows={len(rows)}")
        elif op == "synthesize":
            messages = assemble_context(state)
            use_large = state.intent in ("law",) or (state.intent_conf < 0.6 and (state.rag_results or state.jira_results))
            llm = svc.llm_large if use_large else svc.llm_small
            raw = llm.call(model=("235B" if use_large else "32B"), messages=messages, max_tokens=1200)
            state.answer_draft = raw
            state.events.append(f"synth:model={'large' if use_large else 'small'}")
        else:
            state.events.append(f"unknown_step:{op}")
    return state