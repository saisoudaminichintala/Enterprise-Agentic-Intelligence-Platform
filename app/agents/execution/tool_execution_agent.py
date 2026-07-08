from app.graph.state import AgentState
from app.tools.tool_registry import ToolRegistry

tool_registry = ToolRegistry()


def tool_executor_node(state: AgentState):
    """
    Executes selected tool through ToolRegistry.

    It does not directly instantiate tools.
    This keeps execution loosely coupled and extensible.
    """

    if state["approval_status"] == "WAITING_FOR_HUMAN_APPROVAL":
        result = "Tool execution paused. Waiting for human approval."
    else:
        tool = tool_registry.get_tool(state["selected_tool"])
        tool_response = tool.execute(state["tool_input"])
        result = str(tool_response)

    return {
        "tool_result": result,
        "agents_used": state["agents_used"] + ["tool_executor_agent"],
    }