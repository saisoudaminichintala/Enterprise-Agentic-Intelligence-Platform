from app.agents.execution.tool_executor_agent import tool_executor_node


def test_executes_web_search():
    state = {
        "selected_tool": "web_search",
        "tool_input": {
            "query": "LangGraph official documentation"
        },
        "agents_used": ["tool_selector_llm"],
    }

    result = tool_executor_node(state)

    print(result)

    assert result["tool_result"]["success"] is True
    assert result["tool_result"]["tool"] == "web_search"
    assert len(result["tool_result"]["results"]) > 0
    assert "tool_executor_agent" in result["agents_used"]


def test_executes_calculator_with_calculation_input():
    state = {
        "selected_tool": "calculator",
        "tool_input": {
            "calculation": "2 + 3 * 4"
        },
        "agents_used": ["tool_selector_llm"],
    }

    result = tool_executor_node(state)

    assert result["tool_result"]["status"] == "SUCCESS"
    assert result["tool_result"]["tool"] == "calculator"
    assert result["tool_result"]["result"] == 14
    assert "tool_executor_agent" in result["agents_used"]


def test_generic_tool_transforms_uppercase_text():
    state = {
        "selected_tool": "generic_tool",
        "tool_input": {
            "input_text": (
                "Convert the following text to uppercase: "
                "Enterprise Agentic Intelligence Platform"
            )
        },
        "agents_used": ["tool_selector_llm"],
    }

    result = tool_executor_node(state)

    assert result["tool_result"]["status"] == "SUCCESS"
    assert result["tool_result"]["tool"] == "generic_tool"
    assert result["tool_result"]["result"] == (
        "ENTERPRISE AGENTIC INTELLIGENCE PLATFORM"
    )


def test_handles_unknown_tool_with_registry_fallback():
    state = {
        "selected_tool": "invented_tool",
        "tool_input": {
            "input_text": "Test fallback"
        },
        "agents_used": [],
    }

    result = tool_executor_node(state)

    assert "tool_result" in result
    assert "tool_executor_agent" in result["agents_used"]