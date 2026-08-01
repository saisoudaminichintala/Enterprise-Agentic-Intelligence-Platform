from typing import Any
from app.tools.base_tool import BaseTool


class GenericTool(BaseTool):
    name = "generic_tool"
    description = "Fallback tool for simulated execution."

    def execute(self, **kwargs: Any) -> dict[str, Any]:
        input_data = kwargs.get("input_data", kwargs)
        text = ""

        if isinstance(input_data, dict):
            text = str(input_data.get("input_text") or input_data.get("text") or "").strip()
        elif isinstance(input_data, str):
            text = input_data.strip()

        if "uppercase" in text.lower() and ":" in text:
            actual_text = text.split(":", 1)[-1].strip()
            result = actual_text.upper()
        elif "lowercase" in text.lower() and ":" in text:
            actual_text = text.split(":", 1)[-1].strip()
            result = actual_text.lower()
        else:
            result = "Generic tool execution simulated successfully."

        return {
            "tool": self.name,
            "status": "SUCCESS",
            "result": result,
            "input": input_data
        }