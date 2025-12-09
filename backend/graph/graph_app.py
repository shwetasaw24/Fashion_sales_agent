from langgraph.graph import StateGraph, END

from .state import AgentState
from .nodes import router_node, reply_node


def build_graph():

    graph = StateGraph(AgentState)

    graph.add_node("router", router_node)
    graph.add_node("reply", reply_node)

    graph.set_entry_point("router")

    graph.add_edge("router", "reply")
    graph.add_edge("reply", END)

    return graph.compile()


langgraph_app = build_graph()
