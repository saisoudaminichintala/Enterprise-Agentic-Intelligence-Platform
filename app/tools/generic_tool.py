from typing import Any, Dict
from app.tools.base_tool import BaseTool


class GenericTool(BaseTool):
    name = "generic_tool"
    description = "Fallback tool for simulated execution."

    def execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        return {
            "tool": self.name,
            "status": "SUCCESS",
            "result": "Generic tool execution simulated successfully.",
            "input": input_data
        }