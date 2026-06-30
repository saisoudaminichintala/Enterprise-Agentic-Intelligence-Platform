from app.graph.state import AgentState

def request_router_node(state: AgentState):
    """
    Decides what kind of request this is.

    Later:
    - RAG question
    - Tool execution
    - General chat
    - Workflow request
    """

    return {
        "route": "knowledge",
        "agents_used": state["agents_used"] + ["request_router"]
    }

def master_supervisor_node(state: AgentState):
    """
    Main supervisor node.

    Later:
    - Decides whether to use knowledge supervisor,
      reasoning supervisor, or execution supervisor.
    """

    return {
        "agents_used": state["agents_used"] + ["master_supervisor"]
    }

def planner_node(state: AgentState):
    """
    Creates a plan for answering the user question.
    """

    return {
        "plan": [
            "Understand user question",
            "Retrieve relevant knowledge",
            "Generate final response"
        ],
        "agents_used": state["agents_used"] + ["planner_agent"]
    }

def retriever_node(state: AgentState):
    """
    Dummy retriever node.

    Later:
    - Call RAG service
    - Search vector DB
    - Return relevant document chunks
    """

    return {
        "retrieved_docs": [
            "Dummy document chunk 1",
            "Dummy document chunk 2"
        ],
        "agents_used": state["agents_used"] + ["retriever_agent"]
    }

def response_composer_node(state: AgentState):
    """
    Creates the final answer.
    """

    return {
        "final_answer": (
            f"Dummy graph response for: {state['question']}. "
            f"Used docs: {state['retrieved_docs']}"
        ),
        "agents_used": state["agents_used"] + ["response_composer"]
    }