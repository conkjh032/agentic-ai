import time
from ..util.types import AgentState
from ..services.llm import LLMClient
from ..nodes.act import Services

LTM_STORE = {}


# 단기 및 장기 기억 업데이트
def node_mem(state: AgentState, svc: Services) -> AgentState:
    # 최근 대화 요약 생성 (단기 기억용)
    tldr_prompt = [
        {"role": "system", "content": "Summarize the conversation update in <=2 bullet lines."},
        {"role": "user", "content": f"Q: {state.user_query}\nA(draft): {state.answer_draft[:600]}"}
    ]
    tldr = svc.llm_small.call(model="32B", messages=tldr_prompt, max_tokens=120)

    # 단기 기억(STM) 업데이트 (최근 대화 요약 저장)
    state.stm_summary.append(tldr)
    if len(state.stm_summary) > 6:
        state.stm_summary = state.stm_summary[-3:]

    # 장기 기억(LTM) 업데이트 (예: 자주 사용하는 JQL 패턴 저장)
    if state.intent == "jira" and state.jira_results:
        key = f"ltm:{state.user_id}:fav_jql"
        LTM_STORE[key] = {"jql_example": "project = DEMO AND text ~ '…'", "updated_at": time.time()}
        state.ltm_keys.append(key)

    # 최종 답변 확정
    state.answer_final = state.answer_draft
    state.events.append("mem:stm_updated+ltm_checked")
    return state