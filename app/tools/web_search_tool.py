from typing import Any

from tavily import TavilyClient

from app.config.settings import settings
from app.tools.base_tool import BaseTool


class WebSearchTool(BaseTool):
    """
    Searches the public web using Tavily.

    The tool returns a provider-independent structure so agents do not depend
    directly on Tavily's raw SDK response.
    """

    def __init__(self) -> None:
        self.client = TavilyClient(
            api_key=settings.tavily_api_key.get_secret_value()
        )

    @property
    def name(self) -> str:
        return "web_search"

    @property
    def description(self) -> str:
        return (
            "Searches the public web for current information, recent events, "
            "technical documentation, and external knowledge."
        )

    def execute(self, **kwargs: Any) -> dict[str, Any]:
        query = str(kwargs.get("query", "")).strip()

        if not query:
            return {
                "success": False,
                "tool": self.name,
                "error": "Search query is required.",
                "results": [],
            }

        try:
            response = self.client.search(
                query=query,
                search_depth="basic",
                max_results=5,
                include_answer=False,
            )

            results = [
                {
                    "title": result.get("title", ""),
                    "url": result.get("url", ""),
                    "content": result.get("content", ""),
                    "score": result.get("score"),
                }
                for result in response.get("results", [])
            ]

            return {
                "success": True,
                "tool": self.name,
                "query": query,
                "results": results,
            }

        except Exception as exc:
            return {
                "success": False,
                "tool": self.name,
                "query": query,
                "error": str(exc),
                "results": [],
            }