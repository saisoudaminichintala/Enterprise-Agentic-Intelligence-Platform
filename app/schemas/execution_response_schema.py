from typing import Any

from pydantic import BaseModel, Field


class ExecutionSource(BaseModel):
    title: str = ""
    url: str = ""
    description: str = ""


class ExecutionResponse(BaseModel):
    answer: str = Field(
        ...,
        min_length=1,
        description=(
            "A complete user-facing answer based only on the tool result."
        ),
    )

    summary: str = Field(
        ...,
        min_length=1,
        description="A concise summary of the executed operation.",
    )

    sources: list[ExecutionSource] = Field(
        default_factory=list,
        description="Sources extracted from the tool result when available.",
    )

    metadata: dict[str, Any] = Field(
        default_factory=dict,
        description="Optional execution metadata.",
    )