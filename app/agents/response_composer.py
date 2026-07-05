from app.graph.state import AgentState


def response_composer_node(state: AgentState):
    """
    Final response composer.

    It takes the final state of the agent and composes a response that includes
    the original question, the selected route, and any relevant metadata from the
    agents that were used to arrive at the final answer.
    """

    route = state["route"]

    router_metadata = (
        f"Router confidence: {state['router_confidence']}. "
        f"Router reason: {state['router_reason']}. "
    )

    if route == "knowledge":
        answer = (
            router_metadata
            + f"Knowledge response for: {state['question']}. "
            + f"Knowledge execution plan: {state['knowledge_execution_plan']}. "
            + f"Rewritten query: {state['rewritten_query']}. "
            + f"Query rewrite reason: {state['query_rewrite_reason']}. "
            + f"Cache hit: {state['cache_hit']}. "
            + f"Retrieved docs: {state['retrieved_docs']}. "
            + f"Document grade reason: {state['document_grade_reason']}. "
            + f"Citations: {state['citations']}."
        )

    elif route == "execution":
        answer = (
            router_metadata
            + f"Execution response for: {state['question']}. "
            + f"Master strategy: {state['execution_strategy']}. "
            + f"Workflow strategy: {state['workflow_strategy']}. "
            + f"Workflow plan: {state['plan']}."
        )

    elif route == "reasoning":
        answer = (
            router_metadata
            + f"Reasoning response for: {state['question']}. "
            + f"Master strategy: {state['execution_strategy']}. "
            + f"Reasoning strategy: {state['reasoning_strategy']}. "
            + f"Reasoning plan: {state['plan']}."
        )

    else:
        answer = (
            router_metadata
            + (state["final_answer"] or f"General response for: {state['question']}")
        )

    return {
        "final_answer": answer,
        "agents_used": state["agents_used"] + ["response_composer"],
    }