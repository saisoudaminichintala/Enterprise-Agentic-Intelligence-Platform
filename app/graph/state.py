from typing import TypedDict, List, Optional


class AgentState(TypedDict):
    """
    Shared state passed between all LangGraph nodes.
    Every node reads from it and returns updates to it.
    """

    question: str
    route: Optional[str]
    plan: List[str]
    retrieved_docs: List[str]
    final_answer: Optional[str]
    agents_used: List[str]