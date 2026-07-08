from typing import Any, Dict
from app.tools.base_tool import BaseTool


class CalculatorTool(BaseTool):
    name = "calculator"
    description = "Performs simple arithmetic calculations."

    def execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        expression = input_data.get("expression", "")

        try:
            result = eval(expression, {"__builtins__": {}}, {})
            return {
                "tool": self.name,
                "status": "SUCCESS",
                "result": result
            }
        except Exception as error:
            return {
                "tool": self.name,
                "status": "FAILED",
                "error": str(error)
            }