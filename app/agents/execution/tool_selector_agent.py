from app.graph.state import AgentState


def tool_selector_node(state: AgentState):
    """
    Selects the tool based on the execution plan.

    Later:
    - This can become LLM-powered.
    - It can choose among GitHub, Jira, SQL, email, browser, calculator, etc.
    """

    execution_plan = state["execution_plan"]

    selected_tool = execution_plan.get("tool_needed", "generic_tool")

    if selected_tool == "none":
        selected_tool = "generic_tool"

    tool_input = {
        "question": state["question"],
        "plan": execution_plan,
        "expression": "1 + 1" if selected_tool == "calculator" else ""
    }

    return {
        "selected_tool": selected_tool,
        "tool_input": tool_input,
        "agents_used": state["agents_used"] + ["tool_selector_agent"],
    }