from app.graph.state import AgentState


def response_composer_node(state: AgentState):
    route = state["route"]

    if route == "knowledge":
        answer = (
            f"Knowledge route response for: {state['question']}. "
            f"Retrieved docs: {state['retrieved_docs']}"
        )
    elif route == "execution":
        answer = (
            f"Execution route response for: {state['question']}. "
            f"Workflow plan: {state['plan']}"
        )
    elif route == "reasoning":
        answer = (
            f"Reasoning route response for: {state['question']}. "
            f"Plan: {state['plan']}"
        )
    else:
        answer = state["final_answer"] or f"General response for: {state['question']}"

    return {
        "final_answer": answer,
        "agents_used": state["agents_used"] + ["response_composer"]
    }