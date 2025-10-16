from typing import List, Dict, Any
from .types import AgentState
from .config import SOFT_BUDGET

def assemble_context(state: AgentState) -> List[Dict[str, str]]:
    system = (
        "You are an enterprise assistant. Include sources/citations for factual claims. "
        "Mask PII/internal IDs. Use concise bullets, then a short summary and next-actions."
    )
    stm = "\n".join(state.stm_summary[-3:]) if state.stm_summary else ""

    def fmt_docs(docs):
        parts = []
        for d in docs[:5]:
            parts.append(f"- {d.get('content','')[:240]} [src: {d.get('source')} p.{d.get('page')}]")
        return "\n".join(parts)

    def fmt_jira(rows):
        parts = []
        for r in rows[:5]:
            parts.append(f"- {r['key']}: {r['summary']} ({r['url']})")
        return "\n".join(parts)

    def fmt_prom(res):
        if not res: return ""
        s = res.get("stats", {})
        return f"avg={s.get('avg')}, p95={s.get('p95')}, max={s.get('max')} for {res.get('promql')}"

    context_blobs = []
    if state.rag_results:
        context_blobs.append("RAG:\n" + fmt_docs(state.rag_results))
    if state.jira_results:
        context_blobs.append("Jira:\n" + fmt_jira(state.jira_results))
    if state.prom_results:
        context_blobs.append("Metrics:\n" + fmt_prom(state.prom_results))

    context_str = "\n\n".join([b for b in context_blobs if b])

    messages = [
        {"role": "system", "content": system},
        {"role": "user", "content": f"Short-term summary so far:\n{stm}"},
        {"role": "user", "content": f"Context evidence:\n{context_str}"},
        {"role": "user", "content": f"User question: {state.user_query}"},
        {"role": "user", "content":
            "Return JSON with fields: summary, key_points[], links[], citations[], limitations, next_actions[]."}
    ]

    # TODO: token counting & trimming to respect SOFT_BUDGET
    return messages