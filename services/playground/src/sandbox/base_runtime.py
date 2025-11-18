"""
base_runtime.py

Defines the abstract interface for all sandbox runtimes.
Every runtime (Python, JS, Bash, etc.) MUST inherit this class.

Responsibilities:
- Define how code is executed
- Manage isolated execution context
- Provide a reset() method for clearing runtime state
"""

from abc import ABC, abstractmethod
from typing import Any, Dict


class BaseSandboxRuntime(ABC):
    """
    Abstract base class for language-specific sandbox runtimes.
    """

    def __init__(self):
        # Execution context stores variables, memory, state between runs
        self.context: Dict[str, Any] = {}

    @abstractmethod
    def execute(self, code: str) -> Any:
        """
        Execute arbitrary code in an isolated runtime.

        Args:
            code (str): User-provided code to execute.

        Returns:
            Any: Result of execution (format varies by language).

        Raises:
            Exception: Any runtime-specific execution error.
        """
        pass

    @abstractmethod
    def reset(self) -> None:
        """
        Clear the execution context and reset runtime state.
        """
        pass

    def get_context(self) -> Dict[str, Any]:
        """
        Returns the current execution context for debugging or inspection.
        """
        return self.context
