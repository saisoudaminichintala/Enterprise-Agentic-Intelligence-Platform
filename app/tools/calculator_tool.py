from typing import Any
from app.tools.base_tool import BaseTool


class CalculatorTool(BaseTool):
    name = "calculator"
    description = "Performs simple arithmetic calculations."

    def execute(self, **kwargs: Any) -> dict[str, Any]:
        input_data = kwargs.get("input_data", {})
        if isinstance(input_data, dict):
            expression = input_data.get("expression", input_data.get("calculation", ""))
        else:
            expression = ""

        expression = str(kwargs.get("expression", kwargs.get("calculation", expression))).strip()

        if not expression:
            return {
                "tool": self.name,
                "status": "FAILED",
                "error": "Expression is required."
            }

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