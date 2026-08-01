from typing import Any

from app.graph.state import AgentState
from app.tools.tool_registry import ToolRegistry


tool_registry = ToolRegistry()


def tool_executor_node(state: AgentState) -> dict[str, Any]:
    """
    Retrieves the selected tool from the registry and executes it.
    """

    selected_tool = state.get("selected_tool", "generic_tool")
    tool_input = state.get("tool_input", {})
    agents_used = state.get("agents_used", [])

    tool = tool_registry.get_tool(selected_tool)

    try:
        result = tool.execute(**tool_input)

    except Exception as exc:
        result = {
            "success": False,
            "tool": selected_tool,
            "error": str(exc),
        }

    return {
        "tool_result": result,
        "agents_used": agents_used + ["tool_executor_agent"],
    }