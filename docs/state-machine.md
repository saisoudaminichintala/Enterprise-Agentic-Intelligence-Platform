# State Machine

> How LangGraph manages workflow state across supervisors and agents.

---

## Overview

The platform uses LangGraph to coordinate multiple agents through a shared state object called `AgentState`.

Instead of passing independent values between every node, the graph maintains one structured state that is updated as the request moves through the workflow.

This makes agent execution easier to trace, route, and debug.

---

## Why Shared State?

A multi-agent workflow needs a consistent way to share information.

The state may contain:

* Original user question
* Rewritten query
* Selected route
* Retrieved documents
* Citations
* Final answer
* Agents used
* Cache status
* Planning results
* Tool execution results

Each node reads the fields it needs and returns only the fields it updates.

---

## Example AgentState

A simplified state may look like this:

```python
class AgentState(TypedDict):
    run_id: str
    question: str
    rewritten_query: str
    route: str
    cache_hit: bool
    retrieved_documents: list
    relevant_documents: list
    citations: list
    final_answer: str
    agents_used: list[str]
```

The actual state can grow as new capabilities are added.

---

## State Flow

```text
User Question
      │
      ▼
Initial AgentState
      │
      ▼
Request Router
      │
      ▼
Master Supervisor
      │
      ▼
Domain Supervisor
      │
      ▼
Specialized Agents
      │
      ▼
Final AgentState
      │
      ▼
API Response
```

---

## Node Updates

Each LangGraph node should update only the fields it owns.

For example, the cache checker may return:

```python
return {
    "cache_hit": cache_hit,
    "agents_used": state["agents_used"] + ["cache_checker_agent"]
}
```

The retriever may update:

```python
return {
    "retrieved_documents": documents,
    "agents_used": state["agents_used"] + ["retriever_agent_qdrant"]
}
```

The response composer may update:

```python
return {
    "final_answer": answer,
    "agents_used": state["agents_used"] + ["response_composer_llm"]
}
```

This keeps state changes predictable.

---

## Conditional Routing

LangGraph uses conditional edges to decide which node should run next.

Example:

```python
def route_after_cache(state: AgentState) -> str:
    if state.get("cache_hit"):
        return "cache_hit"

    return "cache_miss"
```

The graph can then map those results:

```python
graph.add_conditional_edges(
    "cache_checker",
    route_after_cache,
    {
        "cache_hit": "citation_agent",
        "cache_miss": "retriever_agent"
    }
)
```

This makes routing logic explicit and easy to debug.

---

## Fresh State Per Request

Every new agent request should begin with a fresh state object.

Example:

```python
initial_state = {
    "run_id": run_id,
    "question": question,
    "rewritten_query": "",
    "route": "",
    "cache_hit": False,
    "retrieved_documents": [],
    "relevant_documents": [],
    "citations": [],
    "final_answer": "",
    "agents_used": []
}
```

This prevents values from previous runs from affecting new requests.

---

## Why `agents_used` Matters

The `agents_used` field provides a simple execution trace.

Example:

```json
[
  "request_router_llm",
  "master_supervisor",
  "knowledge_supervisor_llm",
  "query_rewriter_llm",
  "cache_checker_agent",
  "retriever_agent_qdrant",
  "document_grader_llm",
  "citation_agent",
  "response_composer_llm"
]
```

This helps confirm:

* Which route was selected
* Whether retrieval occurred
* Whether an agent was skipped
* Where an incorrect workflow began

---

## State Ownership

A useful rule is that each field should have a clear owner.

| State Field           | Primary Owner                |
| --------------------- | ---------------------------- |
| `route`               | Request Router or Supervisor |
| `rewritten_query`     | Query Rewriter               |
| `cache_hit`           | Cache Checker                |
| `retrieved_documents` | Retriever                    |
| `relevant_documents`  | Document Grader              |
| `citations`           | Citation Agent               |
| `final_answer`        | Response Composer            |
| `agents_used`         | All executed nodes           |

Clear ownership reduces accidental overwrites.

---

## Future State Extensions

The state may later include:

* Guardrail results
* Confidence scores
* Tool execution output
* Human approval status
* Token usage
* Model metadata
* Evaluation scores
* Error details
* Retry count
* Workflow checkpoint information

These fields should be added only when they support a real workflow requirement.

---

## Conclusion

`AgentState` is the shared memory of the LangGraph workflow.

It allows supervisors and agents to coordinate through explicit fields, controlled updates, and conditional routing. This structure makes the platform easier to debug, test, and extend as new tools, guardrails, evaluations, and observability features are added.
