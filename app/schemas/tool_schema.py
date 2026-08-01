from typing import Any

from pydantic import BaseModel, Field


class ToolSelection(BaseModel):
    selected_tool: str = Field(
        description="Exact name of the selected registered tool"
    )
    reason: str = Field(
        description="Short explanation for selecting the tool"
    )
    tool_input: dict[str, Any] = Field(
        default_factory=dict,
        description="Arguments that should be passed to the selected tool",
    )