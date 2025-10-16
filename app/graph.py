from langgraph.graph import StateGraph, END
from langgraph.checkpoint.sqlite import SqliteSaver
from .util.types import AgentState
from .nodes.route import node_route
from .nodes.plan import node_plan
from .nodes.act import node_act, Services
from .nodes.reflect import node_reflect
from .nodes.mem import node_mem
from .util.config import DB_PATH


def build_graph(svc: Services):
    g = StateGraph(AgentState)
    def wrap(fn):
        def _inner(state: AgentState):
            return fn(state, svc)
        return _inner
    
    # 노드 추가
    g.add_node("route", node_route)
    g.add_node("plan", node_plan)
    g.add_node("act", wrap(node_act))
    g.add_node("reflect", wrap(node_reflect))
    g.add_node("mem", wrap(node_mem))
    g.set_entry_point("route")

    # 엣지 추가
    g.add_edge("route", "plan")
    g.add_edge("plan", "act")
    g.add_edge("act", "reflect")
    g.add_edge("reflect", "mem")
    g.add_edge("mem", END)
    checkpointer = SqliteSaver(DB_PATH)
    return g.compile(checkpointer=checkpointer)