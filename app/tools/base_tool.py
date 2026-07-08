from abc import ABC, abstractmethod
from typing import Any, Dict


class BaseTool(ABC):
    """
    Base class for all tools.

    Every tool should follow the same contract:
    - name
    - description
    - execute()
    """

    name: str
    description: str

    @abstractmethod
    def execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        pass