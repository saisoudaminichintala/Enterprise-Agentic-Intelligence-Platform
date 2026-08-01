import json
from groq import Groq

from app.config.settings import settings
from pydantic import BaseModel, ValidationError
from typing import TypeVar
import json

from app.schemas.execution_response_schema import ExecutionResponse

T = TypeVar("T", bound=BaseModel)

class LLMService:
    """
    Central LLM client for the platform.

    For now:
    - Uses Groq
    - Supports JSON routing responses

    Later:
    - Can add retries
    - Add timeout handling
    - Add fallback models
    - Add tracing
    """

    def __init__(self) -> None:
        if settings.groq_api_key is None:
            raise ValueError(
                "GROQ_API_KEY is missing. Set it in the .env file."
            )

        self.client = Groq(
            api_key=settings.groq_api_key.get_secret_value()
        )
        self.model = settings.groq_model
       
    def classify_route(self, question: str) -> dict:
        system_prompt = """
        You are the request router for an enterprise multi-agent AI platform.

        Classify the user's request into exactly one route:

        knowledge:
        Use when the answer must come from uploaded documents, indexed knowledge,
        retrieval, or document citations.

        reasoning:
        Use when the request requires deeper analysis, comparison, planning,
        criticism, reflection, or verification.

        execution:
        Use only when the request requires an external or deterministic tool,
        such as:
        - web search
        - calculator
        - SQL query
        - GitHub operation
        - API call
        - file operation
        - workflow execution
        - external system action

        general:
        Use for:
        - greetings
        - direct questions
        - rewriting
        - summarization
        - translation
        - formatting
        - tone changes
        - text transformations
        - simple explanations that do not require retrieval or tools

        Examples:
        - "What does the uploaded document say about RAG?" -> knowledge
        - "Compare RAG and fine-tuning." -> reasoning
        - "Calculate 1250 divided by 25." -> execution
        - "Search the web for the latest LangGraph release." -> execution
        - "Convert this text to uppercase." -> general
        - "Rewrite this professionally." -> general
        - "Hello." -> general

        Return valid JSON only:

        {
        "route": "knowledge | reasoning | execution | general",
        "confidence": 0.0,
        "reason": "short explanation"
}
"""

        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {
                    "role": "system",
                    "content": system_prompt,
                },
                {
                    "role": "user",
                    "content": question,
                },
            ],
            temperature=0,
            response_format={"type": "json_object"},
        )

        content = response.choices[0].message.content

        if not content:
            return {
                "route": "general",
                "confidence": 0.0,
                "reason": "The router returned an empty response.",
            }

        import json
        return json.loads(content)
    def rewrite_query(self, question: str) -> dict:
        system_prompt = """
    You are a query rewriting agent for an enterprise RAG system.

    Your job:
    - Convert the user's question into a clear retrieval query.
    - Preserve important domain terms.
    - Remove conversational filler.
    - Do not answer the question.
    - Do not add facts that are not in the question.

    Return only valid JSON with this exact structure:
    {
    "rewritten_query": "clean retrieval query",
    "reason": "short explanation"
    }
    """

        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": question},
            ],
            temperature=0.1,
            response_format={"type": "json_object"},
        )

        content = response.choices[0].message.content

        try:
            return json.loads(content)
        except json.JSONDecodeError:
            return {
                "rewritten_query": question,
                "reason": "LLM returned invalid JSON. Falling back to original question."
            }
    def grade_documents(self, question: str, documents: list[str]) -> dict:
            system_prompt = """
    You are a document grading agent for an enterprise RAG system.

    Your job:
    - Review retrieved document chunks.
    - Keep only chunks that are relevant to the user's question.
    - Remove irrelevant or low-value chunks.
    - Do not answer the question.

    Return only valid JSON with this exact structure:
    {
    "relevant_documents": ["doc chunk 1", "doc chunk 2"],
    "reason": "short explanation"
    }
    """

            user_prompt = {
                "question": question,
                "documents": documents
            }

            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": json.dumps(user_prompt)},
                ],
                temperature=0.1,
                response_format={"type": "json_object"},
            )

            content = response.choices[0].message.content

            try:
                return json.loads(content)
            except json.JSONDecodeError:
                return {
                    "relevant_documents": documents,
                    "reason": "LLM returned invalid JSON. Falling back to all documents."
                }

    def generate_general_response(self, question: str) -> str:
        system_prompt = """
    You are a helpful assistant for an enterprise agent platform.

    Respond directly to the user's request.
    Keep the answer concise, clear, and natural.
    Do not use tools or mention internal implementation details.
    """

        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": question},
            ],
            temperature=0.2,
        )

        content = response.choices[0].message.content
        if content:
            return content.strip()

        return "I can help with that."

    def create_knowledge_execution_plan(self, question: str) -> dict:
        system_prompt = """
    You are a Knowledge Supervisor for an enterprise multi-agent RAG platform.

    Your job is to create an execution plan for answering knowledge-related questions.

    Return only valid JSON with this exact structure:
    {
    "knowledge_strategy": "document_rag | semantic_search | hybrid_search | general_knowledge",
    "rewrite_query": true,
    "check_cache": true,
    "use_vector_search": true,
    "use_web_search": false,
    "grade_documents": true,
    "generate_citations": true,
    "confidence": 0.0,
    "reason": "short explanation"
    }

    Rules:
    - Use document_rag when the user asks about uploaded PDFs/documents/files.
    - Use semantic_search when the user asks to search internal knowledge.
    - Use hybrid_search when both internal documents and external/latest knowledge may be useful.
    - Use general_knowledge for simple knowledge questions that do not need retrieval.
    - Set use_web_search true only if latest/current/external information is needed.
    - Set generate_citations true when using documents or search.
    - Do not answer the user question.
    """

        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": question},
            ],
            temperature=0.1,
            response_format={"type": "json_object"},
        )

        content = response.choices[0].message.content

        try:
            return json.loads(content)
        except json.JSONDecodeError:
            return {
                "knowledge_strategy": "document_rag",
                "rewrite_query": True,
                "check_cache": True,
                "use_vector_search": True,
                "use_web_search": False,
                "grade_documents": True,
                "generate_citations": True,
                "confidence": 0.0,
                "reason": "Invalid JSON from LLM. Falling back to default document RAG plan."
            }
        
    def compose_knowledge_answer(
    self,
    question: str,
    retrieved_docs: list[str],
    citations: list[str],
) -> dict:
        system_prompt = """
    You are a response composer for an enterprise RAG system.

    Your job:
    - Answer the user's question using the retrieved documents.
    - Be concise and clear.
    - Do not invent facts.
    - If retrieved documents are weak or empty, say that available context is limited.
    - Include citations from the provided citation list.

    Return only valid JSON with this exact structure:
    {
    "answer": "final user-facing answer",
    "confidence": 0.0,
    "reason": "short explanation"
    }
    """

        user_prompt = {
            "question": question,
            "retrieved_docs": retrieved_docs,
            "citations": citations,
        }

        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": json.dumps(user_prompt)},
            ],
            temperature=0.2,
            response_format={"type": "json_object"},
        )

        content = response.choices[0].message.content

        try:
            return json.loads(content)
        except json.JSONDecodeError:
            return {
                "answer": "I could not generate a reliable final answer from the retrieved context.",
                "confidence": 0.0,
                "reason": "LLM returned invalid JSON."
            }
    def create_reasoning_execution_plan(self, question: str) -> dict:
            system_prompt = """
        You are a Reasoning Supervisor for an enterprise multi-agent AI platform.

        Create an execution plan for complex reasoning tasks.

        Return only valid JSON:
        {
        "reasoning_strategy": "comparative_reasoning | system_design | analytical_reasoning | planning_reasoning",
        "decompose_problem": true,
        "critique_answer": true,
        "reflect_and_improve": true,
        "verify_final_answer": true,
        "confidence": 0.0,
        "reason": "short explanation"
        }
        """

            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": question},
                ],
                temperature=0.1,
                response_format={"type": "json_object"},
            )

            return json.loads(response.choices[0].message.content)


    def create_reasoning_draft(self, question: str) -> dict:
        system_prompt = """
    You are a reasoning planner agent.

    Break down the user's problem and create a clear draft answer.

    Return only valid JSON:
    {
    "draft": "reasoned draft answer",
    "reason": "short explanation"
    }
    """

        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": question},
            ],
            temperature=0.2,
            response_format={"type": "json_object"},
        )

        return json.loads(response.choices[0].message.content)


    def critique_reasoning(self, question: str, draft: str) -> dict:
        system_prompt = """
    You are a critic agent.

    Review the draft for:
    - missing assumptions
    - weak reasoning
    - unclear tradeoffs
    - unsupported conclusions

    Return only valid JSON:
    {
    "feedback": "critic feedback",
    "severity": "low | medium | high"
    }
    """

        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": json.dumps({"question": question, "draft": draft})},
            ],
            temperature=0.1,
            response_format={"type": "json_object"},
        )

        return json.loads(response.choices[0].message.content)


    def reflect_and_improve(self, question: str, draft: str, feedback: str) -> dict:
        system_prompt = """
    You are a reflection agent.

    Improve the draft using critic feedback.

    Return only valid JSON:
    {
    "improved_answer": "improved final answer",
    "reflection_notes": "what was improved"
    }
    """

        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": system_prompt},
                {
                    "role": "user",
                    "content": json.dumps({
                        "question": question,
                        "draft": draft,
                        "feedback": feedback
                    }),
                },
            ],
            temperature=0.2,
            response_format={"type": "json_object"},
        )

        return json.loads(response.choices[0].message.content)


    def verify_reasoning_answer(self, question: str, answer: str) -> dict:
        system_prompt = """
    You are a verifier agent.

    Check whether the final answer:
    - addresses the question
    - is logically consistent
    - avoids unsupported claims
    - is clear and useful

    Return only valid JSON:
    {
    "verification_result": "pass | needs_revision",
    "reason": "short explanation"
    }
    """

        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": json.dumps({"question": question, "answer": answer})},
            ],
            temperature=0.1,
            response_format={"type": "json_object"},
        )

        return json.loads(response.choices[0].message.content)
    def create_execution_plan(self, question: str) -> dict:
        system_prompt = """
    You are an Execution Supervisor for an enterprise agentic AI platform.

    Create a safe execution plan for workflow/tool requests.

    Return only valid JSON:
    {
    "workflow_strategy": "tool_execution | approval_required | planning_only",
    "tool_needed": "email | jira | database | github | generic_tool | none",
    "requires_approval": true,
    "risk_level": "low | medium | high",
    "execution_steps": ["step 1", "step 2"],
    "confidence": 0.0,
    "reason": "short explanation"
    }

    Rules:
    - If the request sends, creates, deletes, updates, or changes external systems, approval is required.
    - If the user only asks for a plan, approval is not required.
    - Do not actually execute anything.
    """

        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": question},
            ],
            temperature=0.1,
            response_format={"type": "json_object"},
        )

        return json.loads(response.choices[0].message.content)

    def generate_structured(
        self,
        *,
        system_prompt: str,
        user_prompt: str,
        response_model: type[T],
        ) -> T:
            """
            Generates a JSON response and validates it against a Pydantic model.
            """

            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": system_prompt,
                    },
                    {
                        "role": "user",
                        "content": user_prompt,
                    },
                ],
                temperature=0,
                response_format={"type": "json_object"},
            )

            content = response.choices[0].message.content

            if not content:
                raise ValueError("The LLM returned an empty response.")

            try:
                parsed_content = json.loads(content)
                return response_model.model_validate(parsed_content)

            except json.JSONDecodeError as exc:
                raise ValueError(
                    f"The LLM returned invalid JSON: {content}"
                ) from exc

            except ValidationError as exc:
                raise ValueError(
                    f"The LLM response did not match the expected schema: {content}"
                ) from exc

    def compose_execution_response(
        self,
        *,
        question: str,
        selected_tool: str,
        tool_result: dict,
    ) -> ExecutionResponse:
        """
        Converts a raw tool result into a normalized user-facing response.

        The LLM must use only the supplied tool output and must not invent
        missing facts or sources.
        """

        system_prompt = """
    You are the Execution Response Composer in an enterprise multi-agent system.

    Your responsibility is to convert raw tool output into a clear,
    accurate, user-facing response.

    Rules:

    1. Answer the user's original question.
    2. Use only information contained in the tool result.
    3. Do not invent facts, links, sources, calculations, or execution results.
    4. Clearly state when the tool failed or returned incomplete information.
    5. Preserve important numerical values exactly.
    6. For web-search results, include useful source titles and URLs.
    7. For calculator results, explain the calculation clearly.
    8. For operational tools, summarize what was executed and the result.
    9. Do not expose internal implementation details unless the user asked.
    10. Return output matching the required JSON schema.

    The answer must be ready to show directly to the user.
    """

        user_prompt = f"""
    Original user question:
    {question}

    Selected tool:
    {selected_tool}

    Raw tool result:
    {json.dumps(tool_result, indent=2, default=str)}
    """

        return self.generate_structured(
            system_prompt=system_prompt,
            user_prompt=user_prompt,
            response_model=ExecutionResponse,
        )