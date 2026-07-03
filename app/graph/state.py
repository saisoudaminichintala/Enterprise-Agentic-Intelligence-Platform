from typing import TypedDict, List, Optional


class AgentState(TypedDict):
    question: str

    # Router decision
    route: Optional[str]

    # Master supervisor decision
    selected_supervisor: Optional[str]
    execution_strategy: Optional[str]

    # Shared working fields
    plan: List[str]
    retrieved_docs: List[str]
    final_answer: Optional[str]
    agents_used: List[str]