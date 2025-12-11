from langgraph.graph import StateGraph, END

from .state import AgentState
from .nodes import router_node, processor_node, reply_node


def build_graph():
    """
    Build the LangGraph workflow:
    1. router_node: Analyze intent
    2. processor_node: Execute tasks
    3. reply_node: Generate response
    """

    graph = StateGraph(AgentState)

    # Add nodes
    graph.add_node("router", router_node)
    graph.add_node("processor", processor_node)
    graph.add_node("reply", reply_node)

    # Set entry point
    graph.set_entry_point("router")

    # Define edges
    graph.add_edge("router", "processor")
    graph.add_edge("processor", "reply")
    graph.add_edge("reply", END)

    return graph.compile()


langgraph_app = build_graph()
