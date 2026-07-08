from app.tools.base_tool import BaseTool
from app.tools.calculator_tool import CalculatorTool
from app.tools.generic_tool import GenericTool


class ToolRegistry:
    """
    Central registry for all tools.

    Why this exists:
    - Execution agents should not directly know every tool class.
    - New tools can be added by registering them here.
    - This follows a plugin-style architecture.
    """

    def __init__(self):
        self.tools: dict[str, BaseTool] = {}

        self.register(CalculatorTool())
        self.register(GenericTool())

    def register(self, tool: BaseTool):
        self.tools[tool.name] = tool

    def get_tool(self, tool_name: str) -> BaseTool:
        return self.tools.get(tool_name, self.tools["generic_tool"])

    def list_tools(self):
        return [
            {
                "name": tool.name,
                "description": tool.description
            }
            for tool in self.tools.values()
        ]