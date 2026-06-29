class MetricsService:
    """
    Handles application metrics.

    Later this will track:
    - Total requests
    - Agent runs
    - LLM latency
    - RAG latency
    - Cache hit rate
    - Failed requests
    """

    def get_metrics(self):
        return {
            "total_requests": 0,
            "total_agent_runs": 0,
            "average_latency_ms": 0,
            "cache_hit_rate": 0,
            "failed_requests": 0
        }