from typing import TypedDict, List, Optional


class AgentState(TypedDict):
    question: str

    route: Optional[str]

    selected_supervisor: Optional[str]
    execution_strategy: Optional[str]

    knowledge_strategy: Optional[str]
    reasoning_strategy: Optional[str]
    workflow_strategy: Optional[str]

    plan: List[str]
    retrieved_docs: List[str]
    final_answer: Optional[str]
    agents_used: List[str]