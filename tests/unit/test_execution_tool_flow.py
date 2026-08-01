from app.agents.execution.execution_supervisor import (
    execution_supervisor_node,
)
from app.agents.execution.tool_executor_agent import (
    tool_executor_node,
)
from app.agents.execution.tool_selector_agent import (
    tool_selector_node,
)


def test_execution_flow_with_web_search():
    state = {
        "question": "What are the latest LangGraph updates?",
        "agents_used": [],
    }

    supervisor_result = execution_supervisor_node(state)
    state.update(supervisor_result)

    selector_result = tool_selector_node(state)
    state.update(selector_result)

    executor_result = tool_executor_node(state)
    state.update(executor_result)

    print(state)

    assert state["workflow_strategy"]
    assert state["selected_tool"] == "web_search"
    assert state["tool_result"]["success"] is True

    assert state["agents_used"] == [
        "execution_supervisor_llm",
        "tool_selector_llm",
        "tool_executor_agent",
    ]