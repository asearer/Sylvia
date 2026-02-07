"""
Model Registry
--------------

Central registry for classifier backends.
Allows runtime swapping between mock, HF, OpenAI, or custom local models.
"""

from .utils import DummyClassifier


class ModelRegistry:
    def __init__(self):
        self.models = {
            "routing-classifier": DummyClassifier()
            # "hf-mnli": HFClassifier(...),
            # "openai": OpenAIClassifier(...),
        }

    def get(self, name: str):
        """Retrieve registered model."""
        if name not in self.models:
            raise ValueError(f"Classifier backend not found: {name}")
        return self.models[name]

    def register(self, name: str, model):
        """Add/override backend model."""
        self.models[name] = model
