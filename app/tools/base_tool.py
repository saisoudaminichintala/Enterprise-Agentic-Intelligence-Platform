from abc import ABC, abstractmethod
from typing import Any


class BaseTool(ABC):
    """
    Common contract implemented by every platform tool.

    Each tool exposes identifying metadata and a single execution method.
    """

    @property
    @abstractmethod
    def name(self) -> str:
        """Unique name used by the tool registry and selector."""
        raise NotImplementedError

    @property
    @abstractmethod
    def description(self) -> str:
        """Human-readable description used during tool selection."""
        raise NotImplementedError

    @abstractmethod
    def execute(self, **kwargs: Any) -> dict[str, Any]:
        """
        Execute the tool and return a structured result.

        Tools should return dictionaries rather than raw SDK responses so the
        rest of the application remains independent of the provider.
        """
        raise NotImplementedError