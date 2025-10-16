from ..util.types import AgentState
from ..services.llm import LLMClient
from ..nodes.act import Services
from ..util.context import assemble_context



def node_reflect(state: AgentState, svc: Services) -> AgentState:
    # 증거(evidence) 평가 및 필요시 추가 검색
    evidence = len(state.rag_results) + len(state.jira_results) + (1 if state.prom_results else 0) + len(state.conf_results)
    enough_evidence = evidence >= 2
    draft_len = len(state.answer_draft)
    good_len = draft_len > 120

    # 추가 증거가 필요하다고 판단되면, 가설적 답변을 생성하여 추가 RAG 수행
    if not enough_evidence and state.intent in ("docs", "general", "law"):
        exp_prompt = [
            {"role": "system", "content": "Generate a 1-2 sentence hypothetical answer to expand retrieval keywords."},
            {"role": "user", "content": state.user_query},
        ]
        hypo = svc.llm_small.call(model="32B", messages=exp_prompt, max_tokens=120)
        query2 = f"{state.user_query} {hypo[:80]}"
        more = svc.vectordb.retrieve(query2, top_k=6)
        state.rag_results = (state.rag_results or []) + more
        state.events.append(f"reflect:second_wave_rag+{len(more)}")
        messages = assemble_context(state)
        raw = svc.llm_large.call(model="235B", messages=messages, max_tokens=1200)
        state.answer_draft = raw
        state.events.append("reflect:resynthesized(large)")

    state.confidence = 0.4 + 0.3 * float(enough_evidence) + 0.3 * float(good_len)
    state.done = True
    return state