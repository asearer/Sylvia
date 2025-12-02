"""
Analyzer Provider Interface.

This module defines the abstract base class for all Code Analyzer providers, allowing
easy swapping between different backends (e.g., Mock, DeepHat, SonarQube).
"""

from abc import ABC, abstractmethod
from typing import Dict

class AnalyzerProvider(ABC):
    """
    Abstract base class for Code Analyzer providers.
    """

    @abstractmethod
    def analyze(self, code_snippet: str) -> Dict:
        """
        Analyze code and return insights.

        Args:
            code_snippet (str): Python code snippet.

        Returns:
            dict: Analysis dictionary.
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
