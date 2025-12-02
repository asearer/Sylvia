"""
LLM Provider Interface.

This module defines the abstract base class for all LLM providers, allowing
easy swapping between different backends (e.g., Mock, Ollama, OpenAI).
"""

from abc import ABC, abstractmethod
from typing import List, Dict, Any

class LLMProvider(ABC):
    """
    Abstract base class for Large Language Model providers.
    """

    @abstractmethod
    def generate_response(self, prompt: str, context: List[Dict[str, str]] = None) -> str:
        """
        Generate a response from the LLM.

        Args:
            prompt (str): The user input or prompt.
            context (List[Dict[str, str]], optional): Chat history or context.

        Returns:
            str: The generated response.
        """
        pass

    @property
    @abstractmethod
    def name(self) -> str:
        """
        Get the name of the provider.

        Returns:
            str: The provider name.
        """
        pass
