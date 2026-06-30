from langgraph.graph import StateGraph, START, END

from app.graph.state import AgentState

from app.agents.request_router import request_router_node
from app.agents.master_supervisor import master_supervisor_node
from app.agents.general_responder import general_responder_node
from app.agents.response_composer import response_composer_node

from app.agents.knowledge.knowledge_supervisor import knowledge_supervisor_node
from app.agents.knowledge.planner_agent import knowledge_planner_node
from app.agents.knowledge.retriever_agent import retriever_node

from app.agents.reasoning.reasoning_supervisor import reasoning_supervisor_node
from app.agents.reasoning.planner_agent import reasoning_planner_node
from app.agents.reasoning.critic_agent import critic_node

from app.agents.execution.execution_supervisor import execution_supervisor_node
from app.agents.execution.workflow_planner_agent import workflow_planner_node
from app.agents.execution.human_approval_agent import human_approval_node


def route_request(state: AgentState):
    return state["route"]


def build_agent_graph():
    graph = StateGraph(AgentState)

    graph.add_node("request_router", request_router_node)
    graph.add_node("master_supervisor", master_supervisor_node)

    graph.add_node("general_responder", general_responder_node)

    graph.add_node("knowledge_supervisor", knowledge_supervisor_node)
    graph.add_node("knowledge_planner", knowledge_planner_node)
    graph.add_node("retriever", retriever_node)

    graph.add_node("reasoning_supervisor", reasoning_supervisor_node)
    graph.add_node("reasoning_planner", reasoning_planner_node)
    graph.add_node("critic", critic_node)

    graph.add_node("execution_supervisor", execution_supervisor_node)
    graph.add_node("workflow_planner", workflow_planner_node)
    graph.add_node("human_approval", human_approval_node)

    graph.add_node("response_composer", response_composer_node)

    graph.add_edge(START, "request_router")
    graph.add_edge("request_router", "master_supervisor")

    graph.add_conditional_edges(
        "master_supervisor",
        route_request,
        {
            "knowledge": "knowledge_supervisor",
            "reasoning": "reasoning_supervisor",
            "execution": "execution_supervisor",
            "general": "general_responder",
        }
    )

    graph.add_edge("knowledge_supervisor", "knowledge_planner")
    graph.add_edge("knowledge_planner", "retriever")
    graph.add_edge("retriever", "response_composer")

    graph.add_edge("reasoning_supervisor", "reasoning_planner")
    graph.add_edge("reasoning_planner", "critic")
    graph.add_edge("critic", "response_composer")

    graph.add_edge("execution_supervisor", "workflow_planner")
    graph.add_edge("workflow_planner", "human_approval")
    graph.add_edge("human_approval", "response_composer")

    graph.add_edge("general_responder", "response_composer")
    graph.add_edge("response_composer", END)

    compiled_graph = graph.compile()

    print(compiled_graph.get_graph().draw_mermaid())

    return compiled_graph