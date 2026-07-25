# Folder Structure

> Understanding the organization, responsibilities, and architectural boundaries of the Enterprise Agentic Intelligence Platform.

---

# Table of Contents

1. Introduction
2. Why Project Structure Matters
3. Complete Repository Structure
4. Root Directory
5. Application Layer
6. API Layer
7. Agent Layer
8. Graph Layer
9. Service Layer
10. Infrastructure Layer
11. Configuration Layer
12. Models and Schemas
13. Tests
14. Documentation
15. Dependency Flow
16. Design Principles

---

# Introduction

As AI systems grow beyond simple prototypes, project organization becomes just as important as algorithms and prompts.

A well-designed folder structure improves:

* Maintainability
* Scalability
* Testability
* Developer onboarding
* Team collaboration
* Separation of responsibilities

The Enterprise Agentic Intelligence Platform follows a layered architecture where each directory owns a clearly defined responsibility.

This document explains the purpose of every major directory and how the application is organized.

---

# Why Project Structure Matters

Many AI projects begin as notebooks or small scripts.

While suitable for experimentation, this approach quickly becomes difficult to maintain as the project grows.

Common problems include:

* Business logic mixed with API code
* LLM calls scattered throughout the application
* Duplicate utility functions
* Tight coupling between components
* Difficult testing
* Poor scalability

To avoid these issues, this platform separates responsibilities into independent architectural layers.

---

# Complete Repository Structure

```text
Enterprise-Agentic-Intelligence-Platform/
│
├── app/
│   ├── agents/
│   ├── api/
│   ├── config/
│   ├── core/
│   ├── graph/
│   ├── infrastructure/
│   ├── models/
│   ├── schemas/
│   ├── services/
│   │   ├── business/
│   │   └── infrastructure/
│   └── main.py
│
├── docs/
├── tests/
├── requirements.txt
├── pyproject.toml
├── uv.lock
├── README.md
└── .env
```

---

# Root Directory

The root directory contains project-wide resources.

## README.md

The primary landing page.

Provides:

* Project overview
* Architecture summary
* Technology stack
* Roadmap
* Documentation links

---

## requirements.txt

Lists Python dependencies used by the application.

This enables reproducible environments across different machines.

---

## pyproject.toml

Defines project metadata and dependency management.

Using `pyproject.toml` centralizes package configuration and follows modern Python packaging practices.

---

## uv.lock

Locks dependency versions to ensure consistent installations across development environments.

---

## docs/

Contains detailed technical documentation.

Large engineering decisions are intentionally documented outside the README to keep the landing page concise.

---

## tests/

Contains automated tests.

Testing is organized independently from implementation to encourage maintainability and continuous integration.

---

# app/

The `app` directory contains the complete application source code.

Everything required to run the platform lives inside this directory.

The application is organized into independent architectural layers.

---

# app/main.py

This is the application entry point.

Responsibilities include:

* Creating the FastAPI application
* Registering API routers
* Configuring middleware
* Starting the web server

Business logic should never be implemented here.

---

# api/

The API layer exposes REST endpoints.

Responsibilities include:

* Request validation
* Response serialization
* HTTP status codes
* Dependency injection
* Endpoint definitions

Examples:

* Chat APIs
* Document APIs
* Agent APIs
* Metrics APIs
* Health APIs

The API layer delegates all business operations to services.

---

# agents/

The agents directory contains all AI agents responsible for executing workflows.

Examples include:

* Request Router
* Query Rewriter
* Cache Checker
* Retriever
* Planner
* Critic
* Tool Selector
* Response Composer

Each agent performs a single specialized task.

Agents communicate through the shared `AgentState` managed by LangGraph.

---

# graph/

The graph directory defines the orchestration layer.

Responsibilities include:

* LangGraph construction
* Node registration
* Conditional routing
* State transitions
* Workflow execution
* Supervisor hierarchy

This directory defines how agents collaborate.

It does **not** implement business logic.

---

# services/

The service layer contains reusable application logic.

The project separates services into two categories.

```text
services/
│
├── business/
└── infrastructure/
```

This distinction prevents infrastructure concerns from leaking into business workflows.

---

# services/business/

Business services implement application-specific workflows.

Examples include:

* Chat Service
* Document Service
* RAG Service

Responsibilities:

* Coordinate business operations
* Invoke infrastructure services
* Enforce application rules

Business services should not directly communicate with third-party SDKs.

---

# services/infrastructure/

Infrastructure services encapsulate reusable technical functionality.

Examples include:

* LLM Service
* Embedding Service
* Retriever Service
* Vector Store Service

Responsibilities:

* External integrations
* SDK wrappers
* Technical implementations

This abstraction allows technologies to be replaced without affecting business logic.

---

# infrastructure/

This directory contains lower-level infrastructure components shared across the platform.

Examples may include:

* Qdrant clients
* External API clients
* Utility adapters
* Shared connectors

Keeping infrastructure isolated simplifies dependency management and testing.

---

# config/

The configuration layer centralizes application settings.

Responsibilities include:

* Environment variables
* API keys
* Model configuration
* Vector database configuration
* Runtime settings

Using a centralized configuration service prevents configuration values from being scattered throughout the codebase.

---

# core/

Contains reusable framework-level components.

Examples include:

* Dependency injection
* Common utilities
* Shared constants
* Exception handling
* Logging configuration

The core layer supports the application but does not contain business logic.

---

# schemas/

Schemas define request and response contracts.

Examples include:

* API request models
* API response models
* Validation rules
* Serialization

Pydantic models ensure consistent validation across the platform.

---

# models/

Models represent internal domain objects.

Unlike schemas, models are not necessarily exposed through APIs.

Examples include:

* Agent state
* Internal data structures
* Domain entities

Keeping domain models separate from API schemas improves long-term maintainability.

---

# docs/

The documentation directory contains detailed engineering documentation.

Current documents include:

* Architecture
* Project evolution
* Folder structure
* API documentation
* Supervisors
* Agents
* RAG
* Guardrails
* Evaluation
* Observability
* Deployment

The goal is to document not only *what* the platform does but *why* architectural decisions were made.

---

# tests/

Automated testing is essential for production systems.

The test suite will eventually include:

## Unit Tests

Verify individual services and utilities.

---

## Integration Tests

Validate interactions between multiple components.

---

## API Tests

Verify REST endpoints.

---

## Agent Tests

Validate LangGraph workflows.

---

## Evaluation Tests

Benchmark model quality and retrieval performance.

---

# Dependency Flow

The platform follows a one-directional dependency flow.

```text
Client
   │
API Layer
   │
Business Services
   │
Infrastructure Services
   │
External Systems
```

Higher-level layers depend on abstractions rather than implementation details.

For example:

* APIs should not communicate directly with Qdrant.
* APIs should not invoke the Groq SDK.
* Agents should not instantiate clients directly.

Instead, all external communication is delegated to infrastructure services.

---

# Architectural Boundaries

Each layer has clearly defined responsibilities.

| Layer                   | Responsibility                 |
| ----------------------- | ------------------------------ |
| API                     | HTTP communication             |
| Agents                  | AI decision making             |
| Graph                   | Workflow orchestration         |
| Business Services       | Application workflows          |
| Infrastructure Services | Technical integrations         |
| Configuration           | Runtime settings               |
| Models                  | Internal domain representation |
| Schemas                 | API validation                 |

Maintaining these boundaries keeps the application modular and easier to evolve.

---

# Design Principles

The folder organization follows several software engineering principles.

## Single Responsibility Principle

Every directory owns one major responsibility.

---

## Separation of Concerns

Business logic, orchestration, APIs, and infrastructure remain isolated.

---

## Dependency Inversion

Higher-level components depend on abstractions rather than implementation details.

---

## Loose Coupling

Replacing one implementation (for example, switching vector databases) should require minimal changes outside the infrastructure layer.

---

## High Cohesion

Related functionality is grouped together, making the codebase easier to understand and maintain.

---

# Conclusion

The folder structure of the Enterprise Agentic Intelligence Platform is intentionally designed to mirror the architecture of production backend systems.

Rather than organizing files by technology alone, the project is structured around responsibilities and architectural boundaries. This approach enables easier maintenance, clearer ownership, improved scalability, and smoother integration of future capabilities such as guardrails, evaluation frameworks, observability, enterprise tools, and cloud-native deployment.
