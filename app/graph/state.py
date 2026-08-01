from typing import Any, TypedDict


class AgentState(TypedDict, total=False):
    # Core request and routing
    question: str

    route: str
    router_confidence: float
    router_reason: str

    selected_supervisor: str
    agents_used: list[str]

    # Knowledge branch
    knowledge_execution_plan: dict[str, Any]
    rewritten_query: str
    cache_hit: bool
    retrieved_documents: list[dict[str, Any]]
    graded_documents: list[dict[str, Any]]
    citations: list[dict[str, Any]]
    knowledge_answer: str

    # Reasoning branch
    reasoning_draft: str
    verification_result: str

    # Execution branch
    workflow_strategy: str
    execution_plan: dict[str, Any]
    approval_required: bool
    human_approved: bool

    selected_tool: str
    tool_selection_reason: str
    tool_input: dict[str, Any]
    tool_result: dict[str, Any]

    execution_answer: str
    execution_sources: list[dict[str, Any]]
    execution_summary: str
    execution_composer_error: str

    # General branch
    general_response: str

    # Final output
    final_answer: str