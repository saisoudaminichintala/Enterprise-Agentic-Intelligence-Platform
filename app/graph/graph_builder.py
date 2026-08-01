from langgraph.graph import END, START, StateGraph

from app.agents.execution.execution_supervisor import (
    execution_supervisor_node,
)
from app.agents.execution.human_approval_agent import (
    human_approval_node,
)
from app.agents.execution.tool_executor_agent import (
    tool_executor_node,
)
from app.agents.execution.tool_selector_agent import (
    tool_selector_node,
)
from app.agents.execution.workflow_planner_agent import (
    workflow_planner_node,
)
from app.agents.execution.execution_response_composer import (
    execution_response_composer_node,
)
from app.agents.general_responder import general_responder_node

from app.agents.knowledge.cache_checker_agent import cache_checker_node
from app.agents.knowledge.citation_agent import citation_node
from app.agents.knowledge.document_grader_agent import (
    document_grader_node,
)
from app.agents.knowledge.knowledge_supervisor import (
    knowledge_supervisor_node,
)
from app.agents.knowledge.planner_agent import knowledge_planner_node
from app.agents.knowledge.query_rewriter_agent import query_rewriter_node
from app.agents.knowledge.retriever_agent import retriever_node

from app.agents.master_supervisor import master_supervisor_node
from app.agents.request_router import request_router_node
from app.agents.response_composer import response_composer_node

from app.agents.reasoning.critic_agent import critic_node
from app.agents.reasoning.planner_agent import reasoning_planner_node
from app.agents.reasoning.reasoning_supervisor import (
    reasoning_supervisor_node,
)
from app.agents.reasoning.reflection_agent import reflection_node

from app.graph.state import AgentState
from app.services.infrastructure.llm_service import LLMService


llm_service = LLMService()


# =========================================================
# Reasoning verifier node
# =========================================================

def verifier_node(state: AgentState) -> dict:
    """
    Verifies the reasoning answer produced by the reasoning branch.
    """

    result = llm_service.verify_reasoning_answer(
        question=state.get("question", ""),
        answer=state.get("reasoning_draft", ""),
    )

    return {
        "verification_result": result.get(
            "verification_result",
            "needs_revision",
        ),
        "agents_used": state.get("agents_used", [])
        + ["verifier_agent_llm"],
    }


# =========================================================
# Routing functions
# =========================================================

def route_from_master_supervisor(state: AgentState) -> str:
    """
    Routes the request to the supervisor selected by the
    Master Supervisor.
    """

    selected_supervisor = state.get(
        "selected_supervisor",
        "general_responder",
    )

    allowed_supervisors = {
        "knowledge_supervisor",
        "reasoning_supervisor",
        "execution_supervisor",
        "general_responder",
    }

    if selected_supervisor not in allowed_supervisors:
        return "general_responder"

    return selected_supervisor


def route_after_knowledge_supervisor(state: AgentState) -> str:
    """
    Routes the knowledge branch based on the supervisor's plan.

    At this stage, the normal path is to the knowledge planner.
    This function is retained so the supervisor can later skip
    planning if the architecture requires it.
    """

    plan = state.get("knowledge_execution_plan", {})

    if plan.get("requires_planning", True):
        return "knowledge_planner"

    return "query_rewriter"


def route_after_query_rewriter(state: AgentState) -> str:
    """
    Determines the next knowledge step after query rewriting.

    The execution plan may:
    - check cache,
    - skip cache and retrieve directly,
    - skip both and continue to citation.
    """

    plan = state.get("knowledge_execution_plan", {})

    if plan.get("check_cache", True):
        return "check_cache"

    if plan.get("use_vector_search", True):
        return "retrieve"

    return "citation"


def route_after_cache_check(state: AgentState) -> str:
    """
    Routes based on cache availability and the knowledge plan.
    """

    plan = state.get("knowledge_execution_plan", {})

    if state.get("cache_hit", False):
        return "cache_hit"

    if plan.get("use_vector_search", True):
        return "cache_miss_retrieve"

    return "cache_miss_no_retrieve"


def route_after_retriever(state: AgentState) -> str:
    """
    Determines whether retrieved documents should be graded,
    sent directly to citation generation, or composed immediately.
    """

    plan = state.get("knowledge_execution_plan", {})

    if plan.get("grade_documents", True):
        return "grade_documents"

    if plan.get("generate_citations", True):
        return "citation"

    return "response"


def route_after_workflow_planner(state: AgentState) -> str:
    """
    Sends high-risk execution workflows through human approval.

    Low-risk workflows proceed directly to tool selection.
    """

    if state.get("approval_required", False):
        return "approval_required"

    return "approval_not_required"


# =========================================================
# Graph builder
# =========================================================

def build_agent_graph():
    """
    Builds and compiles the hierarchical multi-agent graph.

    Main flow:

        START
          ↓
        request_router
          ↓
        master_supervisor
          ↓
        selected supervisor branch

    Knowledge branch:

        knowledge_supervisor
          ↓
        knowledge_planner
          ↓
        query_rewriter
          ├── cache_checker
          ├── retriever
          └── citation

        cache_checker
          ├── cache hit → citation
          └── cache miss → retriever or citation

        retriever
          ├── document_grader
          ├── citation
          └── response_composer

        document_grader
          ↓
        citation
          ↓
        response_composer

    Reasoning branch:

        reasoning_supervisor
          ↓
        reasoning_planner
          ↓
        critic
          ↓
        reflection
          ↓
        verifier
          ↓
        response_composer

    execution_supervisor
            ↓
    workflow_planner
            ↓
    approval required?
    ┌─────────────┐
    yes            no
    ↓              ↓
    human_approval  tool_selector
    ↓              ↓
    tool_selector   tool_executor
    ↓              ↓
    tool_executor   execution_response_composer
    ↓
    execution_response_composer
            ↓
    response_composer
            ↓
    END

    General branch:

        general_responder
          ↓
        response_composer

    Final flow:

        response_composer
          ↓
        END
    """

    graph = StateGraph(AgentState)

    # =====================================================
    # Core orchestration nodes
    # =====================================================

    graph.add_node(
        "request_router",
        request_router_node,
    )

    graph.add_node(
        "master_supervisor",
        master_supervisor_node,
    )

    graph.add_node(
        "response_composer",
        response_composer_node,
    )

    # =====================================================
    # General route
    # =====================================================

    graph.add_node(
    "execution_response_composer",
    execution_response_composer_node,
)

    graph.add_node(
        "general_responder",
        general_responder_node,
    )

    # =====================================================
    # Knowledge route nodes
    # =====================================================

    graph.add_node(
        "knowledge_supervisor",
        knowledge_supervisor_node,
    )

    graph.add_node(
        "knowledge_planner",
        knowledge_planner_node,
    )

    graph.add_node(
        "query_rewriter",
        query_rewriter_node,
    )

    graph.add_node(
        "cache_checker",
        cache_checker_node,
    )

    graph.add_node(
        "retriever",
        retriever_node,
    )

    graph.add_node(
        "document_grader",
        document_grader_node,
    )

    graph.add_node(
        "citation",
        citation_node,
    )

    # =====================================================
    # Reasoning route nodes
    # =====================================================

    graph.add_node(
        "reasoning_supervisor",
        reasoning_supervisor_node,
    )

    graph.add_node(
        "reasoning_planner",
        reasoning_planner_node,
    )

    graph.add_node(
        "critic",
        critic_node,
    )

    graph.add_node(
        "reflection",
        reflection_node,
    )

    graph.add_node(
        "verifier",
        verifier_node,
    )

    # =====================================================
    # Execution route nodes
    # =====================================================

    graph.add_node(
        "execution_supervisor",
        execution_supervisor_node,
    )

    graph.add_node(
        "workflow_planner",
        workflow_planner_node,
    )

    graph.add_node(
        "human_approval",
        human_approval_node,
    )

    graph.add_node(
        "tool_selector",
        tool_selector_node,
    )

    graph.add_node(
        "tool_executor",
        tool_executor_node,
    )

    # =====================================================
    # Start flow
    # =====================================================

    graph.add_edge(
        START,
        "request_router",
    )

    graph.add_edge(
        "request_router",
        "master_supervisor",
    )

    # =====================================================
    # Master supervisor routing
    # =====================================================

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

    # =====================================================
    # Knowledge branch
    # =====================================================

    graph.add_conditional_edges(
        "knowledge_supervisor",
        route_after_knowledge_supervisor,
        {
            "knowledge_planner": "knowledge_planner",
            "query_rewriter": "query_rewriter",
        },
    )

    graph.add_edge(
        "knowledge_planner",
        "query_rewriter",
    )

    graph.add_conditional_edges(
        "query_rewriter",
        route_after_query_rewriter,
        {
            "check_cache": "cache_checker",
            "retrieve": "retriever",
            "citation": "citation",
        },
    )

    graph.add_conditional_edges(
        "cache_checker",
        route_after_cache_check,
        {
            "cache_hit": "citation",
            "cache_miss_retrieve": "retriever",
            "cache_miss_no_retrieve": "citation",
        },
    )

    graph.add_conditional_edges(
        "retriever",
        route_after_retriever,
        {
            "grade_documents": "document_grader",
            "citation": "citation",
            "response": "response_composer",
        },
    )

    graph.add_edge(
        "document_grader",
        "citation",
    )

    graph.add_edge(
        "citation",
        "response_composer",
    )

    # =====================================================
    # Reasoning branch
    # =====================================================

    graph.add_edge(
        "reasoning_supervisor",
        "reasoning_planner",
    )

    graph.add_edge(
        "reasoning_planner",
        "critic",
    )

    graph.add_edge(
        "critic",
        "reflection",
    )

    graph.add_edge(
        "reflection",
        "verifier",
    )

    graph.add_edge(
        "verifier",
        "response_composer",
    )

    # =====================================================
    # Execution branch
    # =====================================================

    graph.add_edge(
        "execution_supervisor",
        "workflow_planner",
    )

    graph.add_conditional_edges(
        "workflow_planner",
        route_after_workflow_planner,
        {
            "approval_required": "human_approval",
            "approval_not_required": "tool_selector",
        },
    )

    graph.add_edge(
        "human_approval",
        "tool_selector",
    )

    graph.add_edge(
        "tool_selector",
        "tool_executor",
    )

    graph.add_edge(
    "tool_executor",
    "execution_response_composer",
)

    graph.add_edge(
        "execution_response_composer",
        "response_composer",
    )

    # =====================================================
    # General branch
    # =====================================================

    graph.add_edge(
        "general_responder",
        "response_composer",
    )

    # =====================================================
    # End flow
    # =====================================================

    graph.add_edge(
        "response_composer",
        END,
    )

    compiled_graph = graph.compile()

    print(compiled_graph.get_graph().draw_mermaid())

    return compiled_graph