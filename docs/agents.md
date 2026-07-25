# Agents

> Overview of the specialized AI agents used in the Enterprise Agentic Intelligence Platform.

---

# Overview

The platform follows a multi-agent architecture where each agent performs a single, well-defined task.

Rather than having one large AI prompt handle every responsibility, work is divided among specialized agents coordinated by supervisors.

---

# Knowledge Agents

These agents support Retrieval-Augmented Generation (RAG).

## Request Router

Determines the type of user request and routes it to the appropriate supervisor.

**Input**

* User question

**Output**

* Selected route

---

## Knowledge Planner

Determines the steps required to answer a knowledge-based request.

**Responsibilities**

* Analyze request
* Prepare retrieval workflow

---

## Query Rewriter

Improves the user's question before retrieval.

**Responsibilities**

* Rewrite ambiguous questions
* Optimize semantic search queries

---

## Cache Checker

Determines whether a previous answer can be reused.

**Responsibilities**

* Check cache
* Reduce unnecessary retrieval and LLM calls

---

## Retriever

Searches the vector database for relevant document chunks.

**Responsibilities**

* Generate embeddings
* Query Qdrant
* Return relevant context

---

## Document Grader

Evaluates retrieved documents before they are used by the language model.

**Responsibilities**

* Filter low-quality results
* Select the most relevant context

---

## Citation Agent

Tracks the source of retrieved information.

**Responsibilities**

* Associate answers with source documents
* Prepare citation metadata

---

## Response Composer

Produces the final response using the retrieved context and citations.

**Responsibilities**

* Generate the final answer
* Return a structured response

---

# Reasoning Agents

These agents improve analytical reasoning.

## Planner

Breaks complex problems into smaller steps before execution.

---

## Critic

Reviews intermediate reasoning and identifies weaknesses.

---

## Reflection

Reconsiders previous reasoning to improve answer quality.

---

## Verifier

Performs a final validation before returning the response.

---

# Execution Agents

These agents interact with external tools and workflows.

## Workflow Planner

Creates an execution plan for tool-based tasks.

---

## Tool Selector

Chooses the appropriate tool for the requested operation.

---

## Tool Registry

Maintains the list of available tools and their capabilities.

---

## Tool Executor

Invokes external tools and returns their results.

---

## Human Approval

Pauses execution when manual approval is required before continuing.

---

# Agent Collaboration

A typical knowledge request follows this sequence:

```text
Request Router
      │
      ▼
Knowledge Planner
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

Not every request executes every agent. The workflow depends on the routing decisions made during execution.

---

# Design Principles

The agent architecture follows a few simple principles:

* Each agent has a single responsibility.
* Agents communicate through shared state.
* Supervisors coordinate execution.
* Agents are modular and reusable.
* New agents can be added with minimal changes to existing workflows.

---

# Future Agents

As the platform grows, additional agents may be introduced, including:

* Guardrail Agent
* Hallucination Detector
* Model Evaluator
* RAG Evaluator
* Observability Agent
* Cost Optimizer
* Prompt Optimizer

---

# Conclusion

The platform's multi-agent architecture separates complex workflows into smaller, specialized components. This modular design improves maintainability, simplifies debugging, and makes it easier to extend the platform with new capabilities over time.
