"""
Classifier Service
------------------

Provides a unified interface for running text classification using
pluggable model backends. Supports multi-label metadata, routing, and
confidence scoring.

Consumed by higher-level Sylvia services such as:
- chat interface
- research assistant
- code execution playground
- self-healing system
- alerting subsystems
"""

from typing import Optional
from .schemas import ClassificationResult
from .model_registry import ModelRegistry


class ClassifierService:
    """Facade for classifier logic with support for multiple backend models."""

    def __init__(self, default_model: str = "routing-classifier"):
        self.registry = ModelRegistry()
        self.model = self.registry.get(default_model)

    def classify(self, text: str) -> ClassificationResult:
        """
        Classify text using current backend model.

        Parameters
        ----------
        text : str
            The user input to classify.

        Returns
        -------
        ClassificationResult
            Normalized classification output.
        """
        backend_output = self.model.predict(text)
        return ClassificationResult.from_backend(backend_output)

    def classify_intent(self, text: str) -> str:
        """Shortcut for retrieving the highest-confidence label."""
        result = self.classify(text)
        return result.primary_label

    def route(self, text: str) -> str:
        """
        Determine routing for the Sylvia system (chat, research, alerts, playground).

        Returns
        -------
        str
            The subsystem name.
        """
        result = self.classify(text)
        return result.routing or "unknown"
