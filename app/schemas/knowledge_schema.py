from pydantic import BaseModel


class KnowledgeExecutionPlan(BaseModel):
    knowledge_strategy: str
    rewrite_query: bool
    check_cache: bool
    use_vector_search: bool
    use_web_search: bool
    grade_documents: bool
    generate_citations: bool
    confidence: float
    reason: str