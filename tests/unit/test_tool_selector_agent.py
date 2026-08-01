from app.agents.execution.tool_selector_agent import tool_selector_node


def test_selects_web_search_for_current_information():
    state = {
        "question": "What are the latest LangGraph updates?",
        "agents_used": [],
    }

    result = tool_selector_node(state)

    print(result)

    assert result["selected_tool"] == "web_search"
    assert result["tool_input"]["query"]
    assert "tool_selector_llm" in result["agents_used"]


def test_selects_calculator_for_calculation():
    state = {
        "question": "Calculate 125 multiplied by 48",
        "agents_used": [],
    }

    result = tool_selector_node(state)

    print(result)

    assert result["selected_tool"] == "calculator"
    assert "expression" in result["tool_input"]


def test_returns_registered_tool():
    state = {
        "question": "Explain dependency injection",
        "agents_used": [],
    }

    result = tool_selector_node(state)

    valid_tools = {
        "web_search",
        "calculator",
        "generic_tool",
    }

    assert result["selected_tool"] in valid_tools