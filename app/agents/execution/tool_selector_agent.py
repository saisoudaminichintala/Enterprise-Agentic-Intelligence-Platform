import json

from app.graph.state import AgentState
from app.schemas.tool_schema import ToolSelection
from app.services.infrastructure.llm_service import LLMService
from app.tools.tool_registry import ToolRegistry


tool_registry = ToolRegistry()
llm_service = LLMService()


def tool_selector_node(state: AgentState) -> dict:
    """
    Uses the LLM to select one registered tool and prepare its input.
    """

    question = state.get("question", "").strip()
    agents_used = state.get("agents_used", [])

    available_tools = tool_registry.list_tools()
    available_tool_names = {
        tool["name"] for tool in available_tools
    }

    system_prompt = """
You are the Tool Selector for an enterprise agent platform.

Select exactly one tool from the registered tools.

Rules:
1. Use web_search for current, recent, external, public, or internet information.
2. Use calculator for mathematical calculations.
3. Use generic_tool only when no specialized tool applies.
4. selected_tool must exactly match a registered tool name.
5. Construct tool_input using the selected tool's expected arguments.
6. Return only valid JSON.

Expected format:
{
  "selected_tool": "tool name",
  "reason": "short selection reason",
  "tool_input": {
    "argument": "value"
  }
}
""".strip()

    user_prompt = f"""
User request:
{question}

Registered tools:
{json.dumps(available_tools, indent=2)}
""".strip()

    try:
        selection = llm_service.generate_structured(
            system_prompt=system_prompt,
            user_prompt=user_prompt,
            response_model=ToolSelection,
        )

        if selection.selected_tool not in available_tool_names:
            return {
                "selected_tool": "generic_tool",
                "tool_selection_reason": (
                    "The LLM selected an unregistered tool. "
                    "The generic fallback was applied."
                ),
                "tool_input": {
                    "input_text": question
                },
                "agents_used": agents_used + ["tool_selector_llm"],
            }

        return {
            "selected_tool": selection.selected_tool,
            "tool_selection_reason": selection.reason,
            "tool_input": selection.tool_input,
            "agents_used": agents_used + ["tool_selector_llm"],
        }

    except Exception as exc:
        return {
            "selected_tool": "generic_tool",
            "tool_selection_reason": (
                f"Tool selection failed. Generic fallback applied: {exc}"
            ),
            "tool_input": {
                "input_text": question
            },
            "agents_used": agents_used + ["tool_selector_llm"],
        }