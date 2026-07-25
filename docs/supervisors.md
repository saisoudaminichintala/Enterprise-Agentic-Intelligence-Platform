# Supervisors

> How the platform coordinates specialized AI agents using hierarchical supervisors.

---

# Overview

Instead of allowing every agent to communicate with every other agent, the platform uses a hierarchy of supervisors.

Each supervisor is responsible for a specific domain and delegates work to specialized agents.

This approach keeps the workflow organized, modular, and easier to extend.

---

# Supervisor Hierarchy

```text
                    Request Router
                          │
                          ▼
                 Master Supervisor
        ┌───────────┼───────────┐
        ▼           ▼           ▼
 Knowledge     Reasoning    Execution
 Supervisor    Supervisor   Supervisor
```

---

# Why Use Supervisors?

As the number of agents grows, a single orchestrator becomes difficult to maintain.

Supervisors help by:

* Separating responsibilities
* Reducing workflow complexity
* Improving maintainability
* Making routing decisions easier to understand
* Allowing each domain to evolve independently

---

# Request Router

The Request Router is the first component that processes every request.

Its responsibility is to determine the nature of the user's request and forward it to the appropriate supervisor.

Examples include:

* Knowledge retrieval
* Analytical reasoning
* Tool execution

The router does not answer questions itself.

---

# Master Supervisor

The Master Supervisor coordinates the overall workflow.

Its responsibilities include:

* Receiving routed requests
* Selecting the appropriate domain supervisor
* Managing high-level execution
* Returning the final workflow result

It acts as the central coordinator for the platform.

---

# Knowledge Supervisor

The Knowledge Supervisor manages all Retrieval-Augmented Generation (RAG) workflows.

Typical agents include:

* Knowledge Planner
* Query Rewriter
* Cache Checker
* Retriever
* Document Grader
* Citation Agent
* Response Composer

Its goal is to produce responses grounded in enterprise documents.

---

# Reasoning Supervisor

The Reasoning Supervisor handles requests that require deeper analysis rather than document retrieval.

Typical agents include:

* Planner
* Critic
* Reflection
* Verifier

These agents work together to improve the quality and reliability of generated responses.

---

# Execution Supervisor

The Execution Supervisor manages workflows that interact with external systems or tools.

Typical agents include:

* Workflow Planner
* Tool Selector
* Tool Registry
* Tool Executor
* Human Approval

This supervisor is responsible for safely executing actions outside the language model.

---

# Supervisor Communication

Supervisors do not perform every task themselves.

Instead, they coordinate specialized agents and collect their results.

```text
Knowledge Supervisor
        │
        ▼
 Query Rewriter
        │
        ▼
 Cache Checker
        │
        ▼
 Retriever
        │
        ▼
 Document Grader
        │
        ▼
 Citation Agent
        │
        ▼
 Response Composer
```

This keeps each agent focused on a single responsibility.

---

# Benefits of This Design

Using hierarchical supervisors provides several advantages:

* Clear separation of responsibilities
* Easier debugging
* Independent development of each domain
* Better scalability as new agents are added
* Improved readability of the workflow

---

# Future Enhancements

As the platform evolves, supervisors may support:

* Dynamic agent selection
* Parallel execution
* Confidence-based routing
* Retry strategies
* Workflow checkpoints
* Human-in-the-loop approvals

These enhancements can be added without changing the overall architecture.

---

# Conclusion

Supervisors are responsible for orchestrating the platform's specialized agents.

By organizing the workflow into Knowledge, Reasoning, and Execution domains, the platform remains modular, scalable, and easier to maintain as new capabilities are introduced.
