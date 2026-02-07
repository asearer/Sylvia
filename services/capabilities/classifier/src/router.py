"""
Classifier Router
-----------------

Wraps route determination in a dedicated class so that routing rules can grow
in complexity without polluting the classifier service.
"""

from .classifier_service import ClassifierService


class ClassifierRouter:
    """Apply routing logic on top of classifier predictions."""

    def __init__(self):
        self.classifier = ClassifierService()

    def route(self, text: str) -> str:
        """
        Based on classifier output, route request to the correct Sylvia subsystem.
        """
        result = self.classifier.classify(text)

        # Direct routing from classifier metadata
        if result.routing:
            return result.routing

        # Fallback rules if metadata isn't given
        label = result.primary_label.lower()

        if "research" in label:
            return "research"
        if "code" in label or "developer" in label:
            return "playground"
        if "alert" in label or "bug" in label:
            return "alerts"
        return "chat"
