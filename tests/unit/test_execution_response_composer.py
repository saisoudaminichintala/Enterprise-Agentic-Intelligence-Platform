from unittest.mock import patch

from app.agents.execution.execution_response_composer import (
    execution_response_composer_node,
)
from app.schemas.execution_response_schema import (
    ExecutionResponse,
    ExecutionSource,
)


def test_execution_response_composer_web_search():
    state = {
        "question": "What is LangGraph?",
        "selected_tool": "web_search",
        "tool_result": {
            "success": True,
            "tool": "web_search",
            "results": [
                {
                    "title": "LangGraph Documentation",
                    "url": "https://example.com/langgraph",
                    "content": (
                        "LangGraph is a framework for building "
                        "stateful agent workflows."
                    ),
                }
            ],
        },
        "agents_used": ["tool_executor_agent"],
    }

    mocked_response = ExecutionResponse(
        answer=(
            "LangGraph is a framework for building stateful "
            "agent workflows."
        ),
        summary="Web search results were synthesized successfully.",
        sources=[
            ExecutionSource(
                title="LangGraph Documentation",
                url="https://example.com/langgraph",
                description="Official LangGraph information.",
            )
        ],
    )

    with patch(
        "app.agents.execution.execution_response_composer."
        "llm_service.compose_execution_response",
        return_value=mocked_response,
    ):
        result = execution_response_composer_node(state)

    assert result["execution_answer"]
    assert result["execution_summary"]
    assert len(result["execution_sources"]) == 1

    assert result["execution_sources"][0]["title"] == (
        "LangGraph Documentation"
    )

    assert result["agents_used"] == [
        "tool_executor_agent",
        "execution_response_composer_llm",
    ]


def test_execution_response_composer_handles_tool_failure():
    state = {
        "question": "Search for current LangGraph news",
        "selected_tool": "web_search",
        "tool_result": {
            "success": False,
            "error": "Tavily API request failed.",
        },
        "agents_used": ["tool_executor_agent"],
    }

    result = execution_response_composer_node(state)

    assert "could not be completed" in result["execution_answer"]
    assert "Tavily API request failed" in result["execution_answer"]
    assert result["execution_sources"] == []

    assert result["agents_used"] == [
        "tool_executor_agent",
        "execution_response_composer",
    ]


def test_execution_response_composer_falls_back_for_calculator_results():
    state = {
        "question": "What is 2 + 3 * 4?",
        "selected_tool": "calculator",
        "tool_result": {
            "tool": "calculator",
            "status": "SUCCESS",
            "result": 14,
        },
        "agents_used": ["tool_executor_agent"],
    }

    with patch(
        "app.agents.execution.execution_response_composer."
        "llm_service.compose_execution_response",
        side_effect=ValueError("LLM unavailable"),
    ):
        result = execution_response_composer_node(state)

    assert "14" in result["execution_answer"]
    assert "Calculator returned 14" in result["execution_summary"]
    assert result["execution_sources"] == []
    assert result["agents_used"] == [
        "tool_executor_agent",
        "execution_response_composer_error",
    ]