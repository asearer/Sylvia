"""
Utility helpers + lightweight mock models for testing and development.
"""


class DummyClassifier:
    """
    A deterministic classifier backend so tests are stable.

    Used during early development, and as a failover model if others fail.
    """

    def predict(self, text: str):
        t = text.lower()

        if "bug" in t or "error" in t or "critical" in t:
            return {
                "labels": ["alert", "system"],
                "scores": [0.92, 0.40],
                "meta": {"routing": "alerts"}
            }

        if "research" in t or "find" in t or "information" in t:
            return {
                "labels": ["research", "info"],
                "scores": [0.89, 0.22],
                "meta": {"routing": "research"}
            }

        if "code" in t or "python" in t or "developer" in t:
            return {
                "labels": ["code", "developer"],
                "scores": [0.88, 0.33],
                "meta": {"routing": "playground"}
            }

        return {
            "labels": ["chat"],
            "scores": [0.99],
            "meta": {"routing": "chat"}
        }
