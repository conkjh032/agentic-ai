import uuid
from app.graph import build_graph
from app.nodes.act import Services
from app.services.llm import LLMClient
from app.services.mcp_jira import JiraMCP
from app.services.mcp_confluence import ConfluenceMCP
from app.services.mcp_prometheus import PrometheusMCP
from app.services.vectordb import VectorDB
from app.util.types import AgentState
from app.util.config import (
    LLM_API_KEY, LLM_BASE_URL, JIRA_BASE, CONF_BASE, PROM_BASE, VECTORDB_URL
)


def main():
    # 필요한 서비스 클라이언트 초기화
    svc = Services(
        llm_small=LLMClient(api_key=LLM_API_KEY, base_url=LLM_BASE_URL),
        llm_large=LLMClient(api_key=LLM_API_KEY, base_url=LLM_BASE_URL),
        jira=JiraMCP(base_url=JIRA_BASE, token="demo"),
        conf=ConfluenceMCP(base_url=CONF_BASE, token="demo"),
        prom=PrometheusMCP(base_url=PROM_BASE),
        vectordb=VectorDB(url=VECTORDB_URL),
    )

    # 그래프 빌드
    app = build_graph(svc)

    # 초기 상태 생성
    state = AgentState(
        user_id="user-123",
        session_id=str(uuid.uuid4()),
        user_query="지라에서 지난 주 배포 실패 관련 이슈 찾아줘. 원인 요약도 부탁해.",
    )

    # 그래프 실행
    final: AgentState = app.invoke(state)

    print("=== FINAL ANSWER ===")
    print(final.answer_final)
    print("=== EVENTS ===")
    print("".join(final.events))

if __name__ == "__main__":
    main()