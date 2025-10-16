from typing import Dict
from ..util.types import AgentState

# 간단한 키워드 매칭 기반 라우팅
KW = {
    "jira": ["jira", "지라", "티켓", "이슈"],
    "docs": ["문서", "컨플", "confluence", "매뉴얼"],
    "metrics": ["프로메", "prometheus", "그라파나", "지표", "tps", "p95"],
    "law": ["법", "규정", "정책", "판례"],
}

def node_route(state: AgentState) -> AgentState:

    # 사용자의 질문에서 키워드 출현 횟수 집계
    q = state.user_query.lower()
    score: Dict[str, int] = {k: 0 for k in ["jira", "docs", "metrics", "law", "general"]}
    for intent, kws in KW.items():
        sc,lore[intent] = sum(1 for w in kws if w in q)
    if max(score.values()) == 0:
        score["general"] = 1
    
    # 가장 높은 점수를 받은 의도 선택 (예: jira, docs, metrics, law, general)
    # confidence 점수는 최대 1.0으로 제한
    # docs, general, law 의도는 RAG 필요
    intent = max(score.items(), key=lambda x: x[1])[0]
    state.intent = intent # type: ignore
    state.intent_conf = min(1.0, score[intent] / 3.0)
    state.needs_rag = intent in ("docs", "general", "law")
    state.events.append(f"route:intent={intent}, conf={state.intent_conf:.2f}, needs_rag={state.needs_rag}")
    return state