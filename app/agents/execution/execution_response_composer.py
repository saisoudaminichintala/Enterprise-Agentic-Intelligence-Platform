from typing import Any

from app.graph.state import AgentState
from app.schemas.execution_response_schema import ExecutionResponse
from app.services.infrastructure.llm_service import LLMService


llm_service = LLMService()


def _build_failed_execution_response(
    *,
    selected_tool: str,
    tool_result: dict[str, Any],
) -> dict[str, Any]:
    """
    Produces a deterministic fallback response when the tool reports failure.

    This avoids spending another LLM call on a result that already contains
    a clear execution error.
    """

    error_message = (
        tool_result.get("error")
        or tool_result.get("message")
        or "The tool did not provide an error description."
    )

    return {
        "execution_answer": (
            f"The requested operation could not be completed using "
            f"`{selected_tool}`. {error_message}"
        ),
        "execution_summary": (
            f"Execution with {selected_tool} was unsuccessful."
        ),
        "execution_sources": [],
    }


def _normalize_sources(
    response: ExecutionResponse,
) -> list[dict[str, str]]:
    """
    Converts Pydantic source models into serializable state values.
    """

    return [
        source.model_dump()
        for source in response.sources
    ]


def _build_fallback_response(
    *,
    selected_tool: str,
    tool_result: dict[str, Any],
) -> dict[str, Any]:
    """
    Produces a deterministic response when the LLM-based composer is unavailable.
    """

    if tool_result.get("success") is False or tool_result.get("status") == "FAILED":
        error_message = (
            tool_result.get("error")
            or tool_result.get("message")
            or "The tool did not provide an error description."
        )
        return {
            "execution_answer": (
                f"The requested operation could not be completed using "
                f"`{selected_tool}`. {error_message}"
            ),
            "execution_summary": (
                f"Execution with {selected_tool} was unsuccessful."
            ),
            "execution_sources": [],
        }

    if selected_tool == "calculator":
        result_value = tool_result.get("result")
        if result_value is not None:
            return {
                "execution_answer": (
                    f"The calculation completed successfully. Result: {result_value}"
                ),
                "execution_summary": (
                    f"Calculator returned {result_value}."
                ),
                "execution_sources": [],
            }

    if selected_tool == "web_search":
        results = tool_result.get("results", [])
        if results:
            top_result = results[0]
            title = top_result.get("title") or "Search result"
            url = top_result.get("url") or ""
            description = top_result.get("content") or ""
            if url:
                description = f"{description} ({url})".strip()
            return {
                "execution_answer": (
                    f"I found {len(results)} result(s). {title}: {description}"
                ),
                "execution_summary": (
                    f"Web search returned {len(results)} result(s)."
                ),
                "execution_sources": [],
            }

    result_value = tool_result.get("result")
    if result_value is not None:
        return {
            "execution_answer": (
                f"The requested operation completed successfully. Result: {result_value}"
            ),
            "execution_summary": (
                f"Execution with {selected_tool} completed successfully."
            ),
            "execution_sources": [],
        }

    return {
        "execution_answer": (
            f"The requested operation completed successfully using {selected_tool}."
        ),
        "execution_summary": (
            f"Execution with {selected_tool} completed successfully."
        ),
        "execution_sources": [],
    }


def execution_response_composer_node(
    state: AgentState,
) -> dict[str, Any]:
    """
    Converts heterogeneous raw tool output into a normalized
    execution response.

    Input:
        selected_tool
        tool_result
        question

    Output:
        execution_answer
        execution_summary
        execution_sources
    """

    selected_tool = state.get("selected_tool", "unknown_tool")
    tool_result = state.get("tool_result", {})

    agents_used = state.get("agents_used", [])

    if not tool_result:
        return {
            "execution_answer": (
                "The operation could not be completed because the tool "
                "did not return a result."
            ),
            "execution_summary": "No tool result was available.",
            "execution_sources": [],
            "agents_used": agents_used
            + ["execution_response_composer"],
        }

    if tool_result.get("success") is False:
        failure_response = _build_failed_execution_response(
            selected_tool=selected_tool,
            tool_result=tool_result,
        )

        return {
            **failure_response,
            "agents_used": agents_used
            + ["execution_response_composer"],
        }

    try:
        response = llm_service.compose_execution_response(
            question=state.get("question", ""),
            selected_tool=selected_tool,
            tool_result=tool_result,
        )

        return {
            "execution_answer": response.answer,
            "execution_summary": response.summary,
            "execution_sources": _normalize_sources(response),
            "agents_used": agents_used
            + ["execution_response_composer_llm"],
        }

    except Exception as exc:
        fallback_response = _build_fallback_response(
            selected_tool=selected_tool,
            tool_result=tool_result,
        )

        return {
            **fallback_response,
            "execution_composer_error": str(exc),
            "agents_used": agents_used
            + ["execution_response_composer_error"],
        }