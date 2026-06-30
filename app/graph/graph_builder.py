from langgraph.graph import StateGraph, START, END

from app.graph.state import AgentState


from app.graph.nodes import (
    request_router_node,
    master_supervisor_node,
    planner_node,
    retriever_node,
    response_composer_node,
)
def build_agent_graph():
    """
    Builds the first version of our agent graph.

    Current flow:

    START
      ↓
    request_router
      ↓
    master_supervisor
      ↓
    planner
      ↓
    retriever
      ↓
    response_composer
      ↓
    END
    """

    graph = StateGraph(AgentState)

    graph.add_node("request_router", request_router_node)
    graph.add_node("master_supervisor", master_supervisor_node)
    graph.add_node("planner", planner_node)
    graph.add_node("retriever", retriever_node)
    graph.add_node("response_composer", response_composer_node)

    graph.add_edge(START, "request_router")
    graph.add_edge("request_router", "master_supervisor")
    graph.add_edge("master_supervisor", "planner")
    graph.add_edge("planner", "retriever")
    graph.add_edge("retriever", "response_composer")
    graph.add_edge("response_composer", END)

    return graph.compile()