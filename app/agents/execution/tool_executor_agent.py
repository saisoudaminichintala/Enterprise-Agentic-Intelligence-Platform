from app.graph.state import AgentState


def tool_executor_node(state: AgentState):
    """
    Simulated tool executor.

    Later:
    - call Jira API
    - send email
    - update DB
    - call GitHub API

    For now:
    - if approval is required, do not execute
    - otherwise simulate execution
    """

    if state["approval_status"] == "WAITING_FOR_HUMAN_APPROVAL":
        result = "Tool execution paused. Waiting for human approval."
    else:
        tool = state["execution_plan"].get("tool_needed", "generic_tool")
        result = f"Simulated execution completed using tool: {tool}"

    return {
        "tool_result": result,
        "agents_used": state["agents_used"] + ["tool_executor_agent"],
    }