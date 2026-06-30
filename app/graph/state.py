from typing import TypedDict, List, Optional


class AgentState(TypedDict):
    """
    Shared state passed between all LangGraph nodes.
    """

    question: str
    route: Optional[str]
    plan: List[str]
    retrieved_docs: List[str]
    final_answer: Optional[str]
    agents_used: List[str]