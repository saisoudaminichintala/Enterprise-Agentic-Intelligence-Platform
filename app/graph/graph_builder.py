from langgraph import graph
from langgraph.graph import StateGraph, START, END

from app.agents.reasoning.reflection_agent import reflection_node
from app.graph.state import AgentState

from app.agents.request_router import request_router_node
from app.agents.master_supervisor import master_supervisor_node
from app.agents.general_responder import general_responder_node
from app.agents.response_composer import response_composer_node

from app.agents.knowledge.knowledge_supervisor import knowledge_supervisor_node
from app.agents.knowledge.planner_agent import knowledge_planner_node
from app.agents.knowledge.query_rewriter_agent import query_rewriter_node
from app.agents.knowledge.cache_checker_agent import cache_checker_node
from app.agents.knowledge.retriever_agent import retriever_node
from app.agents.knowledge.document_grader_agent import document_grader_node
from app.agents.knowledge.citation_agent import citation_node

from app.agents.reasoning.reasoning_supervisor import reasoning_supervisor_node
from app.agents.reasoning.planner_agent import reasoning_planner_node
from app.agents.reasoning.critic_agent import critic_node

from app.agents.execution.execution_supervisor import execution_supervisor_node
from app.agents.execution.workflow_planner_agent import workflow_planner_node
from app.agents.execution.human_approval_agent import human_approval_node
from app.graph.state import AgentState
from app.services.infrastructure.llm_service import LLMService
from app.agents.execution.tool_executor_agent import tool_executor_node
from app.agents.execution.tool_selector_agent import tool_selector_node

llm_service = LLMService()


def verifier_node(state: AgentState):
    result = llm_service.verify_reasoning_answer(
        question=state["question"],
        answer=state["reasoning_draft"],
    )

    return {
        "verification_result": result.get("verification_result", "needs_revision"),
        "agents_used": state["agents_used"] + ["verifier_agent_llm"],
    }

def route_from_master_supervisor(state: AgentState):
    """
    After the Master Supervisor runs, it sets selected_supervisor.

    This function tells LangGraph which supervisor branch to follow next.
    """

    return state["selected_supervisor"]

def route_after_knowledge_supervisor(state: AgentState):
    plan = state["knowledge_execution_plan"]

    if plan.get("rewrite_query", True):
        return "rewrite_query"

    if plan.get("check_cache", True):
        return "check_cache"

    if plan.get("use_vector_search", True):
        return "retrieve"

    return "citation"


def route_after_query_rewriter(state: AgentState):
    plan = state["knowledge_execution_plan"]

    if plan.get("check_cache", True):
        return "check_cache"

    if plan.get("use_vector_search", True):
        return "retrieve"

    return "citation"


def route_after_cache_check(state: AgentState):
    plan = state["knowledge_execution_plan"]

    if state["cache_hit"]:
        return "cache_hit"

    if plan.get("use_vector_search", True):
        return "cache_miss_retrieve"

    return "cache_miss_no_retrieve"


def route_after_retriever(state: AgentState):
    plan = state["knowledge_execution_plan"]

    if plan.get("grade_documents", True):
        return "grade_documents"

    if plan.get("generate_citations", True):
        return "citation"

    return "response"

def build_agent_graph():
    """
    Builds the hierarchical multi-agent graph.

    Overall flow:

    START
      ↓
    request_router
      ↓
    master_supervisor
      ↓
    conditional route:
        knowledge_supervisor
        reasoning_supervisor
        execution_supervisor
        general_responder

    Knowledge route:
        knowledge_supervisor
          ↓
        knowledge_planner
          ↓
        query_rewriter
          ↓
        cache_checker
          ├── cache_hit  → citation → response_composer
          └── cache_miss → retriever → document_grader → citation → response_composer

    Reasoning route:
        reasoning_supervisor
          ↓
        reasoning_planner
          ↓
        critic
          ↓
        response_composer

    Execution route:
        execution_supervisor
          ↓
        workflow_planner
          ↓
        human_approval
          ↓
        response_composer

    General route:
        general_responder
          ↓
        response_composer

    response_composer
      ↓
    END
    """

    graph = StateGraph(AgentState)

    # -----------------------------
    # Core orchestration nodes
    # -----------------------------
    graph.add_node("request_router", request_router_node)
    graph.add_node("master_supervisor", master_supervisor_node)
    graph.add_node("response_composer", response_composer_node)

    # -----------------------------
    # General route
    # -----------------------------
    graph.add_node("general_responder", general_responder_node)

    # -----------------------------
    # Knowledge route nodes
    # -----------------------------
    graph.add_node("knowledge_supervisor", knowledge_supervisor_node)
    graph.add_node("knowledge_planner", knowledge_planner_node)
    graph.add_node("query_rewriter", query_rewriter_node)
    graph.add_node("cache_checker", cache_checker_node)
    graph.add_node("retriever", retriever_node)
    graph.add_node("document_grader", document_grader_node)
    graph.add_node("citation", citation_node)

    # -----------------------------
    # Reasoning route nodes
    # -----------------------------
    graph.add_node("reasoning_supervisor", reasoning_supervisor_node)
    graph.add_node("reasoning_planner", reasoning_planner_node)
    graph.add_node("critic", critic_node)
    graph.add_node("reflection", reflection_node)
    graph.add_node("verifier", verifier_node)

    # -----------------------------
    # Execution route nodes
    # -----------------------------
    graph.add_node("execution_supervisor", execution_supervisor_node)
    graph.add_node("workflow_planner", workflow_planner_node)
    graph.add_node("human_approval", human_approval_node)
    graph.add_node("tool_executor", tool_executor_node)
    graph.add_node("tool_selector", tool_selector_node)

    # -----------------------------
    # Start flow
    # -----------------------------
    graph.add_edge(START, "request_router")
    graph.add_edge("request_router", "master_supervisor")

    # -----------------------------
    # Master supervisor decides main branch
    # -----------------------------
    graph.add_conditional_edges(
        "master_supervisor",
        route_from_master_supervisor,
        {
            "knowledge_supervisor": "knowledge_supervisor",
            "reasoning_supervisor": "reasoning_supervisor",
            "execution_supervisor": "execution_supervisor",
            "general_responder": "general_responder",
        },
    )

    # -----------------------------
    # Knowledge branch
    # -----------------------------
    graph.add_edge("knowledge_supervisor", "knowledge_planner")
    graph.add_edge("knowledge_planner", "query_rewriter")
    graph.add_edge("query_rewriter", "cache_checker")

    graph.add_conditional_edges(
    "cache_checker",
      route_after_cache_check,
      {
          "cache_hit": "citation",
          "cache_miss_retrieve": "retriever",
          "cache_miss_no_retrieve": "citation",
      },
)

    graph.add_edge("retriever", "document_grader")
    graph.add_edge("document_grader", "citation")
    graph.add_edge("citation", "response_composer")

    # -----------------------------
    # Reasoning branch
    # -----------------------------
    graph.add_edge("reasoning_supervisor", "reasoning_planner")
    graph.add_edge("reasoning_planner", "critic")
    graph.add_edge("critic", "reflection")
    graph.add_edge("reflection", "verifier")
    graph.add_edge("verifier", "response_composer")

    # -----------------------------
    # Execution branch
    # -----------------------------
    graph.add_edge("execution_supervisor", "workflow_planner")
    graph.add_edge("workflow_planner", "human_approval")
    graph.add_edge("human_approval", "tool_selector")
    graph.add_edge("tool_selector", "tool_executor")
    graph.add_edge("tool_executor", "response_composer")

    # -----------------------------
    # General branch
    # -----------------------------
    graph.add_edge("general_responder", "response_composer")

    # -----------------------------
    # End flow
    # -----------------------------
    graph.add_edge("response_composer", END)

    compiled_graph = graph.compile()

    # Optional: prints Mermaid graph in terminal
    print(compiled_graph.get_graph().draw_mermaid())

    return compiled_graph