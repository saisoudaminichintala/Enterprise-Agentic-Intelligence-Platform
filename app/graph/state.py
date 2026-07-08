from typing import TypedDict, List, Optional, Dict, Any


class AgentState(TypedDict):
    question: str

    route: Optional[str]
    router_confidence: float
    router_reason: str

    selected_supervisor: Optional[str]
    execution_strategy: Optional[str]

    knowledge_strategy: Optional[str]
    reasoning_strategy: Optional[str]
    workflow_strategy: Optional[str]

    knowledge_execution_plan: Dict[str, Any]

    rewritten_query: Optional[str]
    query_rewrite_reason: str

    cache_hit: bool
    citations: List[str]

    document_grade_reason: str

    plan: List[str]
    retrieved_docs: List[str]
    final_answer: Optional[str]
    agents_used: List[str]
    reasoning_execution_plan: dict
    reasoning_draft: str
    critic_feedback: str
    reflection_notes: str
    verification_result: str

    execution_plan: dict
    approval_required: bool
    approval_status: str
    tool_result: str

    selected_tool: str
    tool_input: dict