from app.graph.state import AgentState


def response_composer_node(state: AgentState):
    route = state["route"]
    strategy = state["execution_strategy"]

    if route == "knowledge":
        answer = (
            f"Knowledge response for: {state['question']}. "
            f"Strategy used: {strategy}. "
            f"Retrieved docs: {state['retrieved_docs']}"
        )

    elif route == "execution":
        answer = (
            f"Execution response for: {state['question']}. "
            f"Strategy used: {strategy}. "
            f"Workflow plan: {state['plan']}"
        )

    elif route == "reasoning":
        answer = (
            f"Reasoning response for: {state['question']}. "
            f"Strategy used: {strategy}. "
            f"Reasoning plan: {state['plan']}"
        )

    else:
        answer = state["final_answer"] or f"General response for: {state['question']}"

    return {
        "final_answer": answer,
        "agents_used": state["agents_used"] + ["response_composer"]
    }