"""
Schemas for classifier outputs.
"""

from dataclasses import dataclass
from typing import List, Dict, Optional


@dataclass
class ClassificationResult:
    labels: List[str]
    scores: List[float]
    primary_label: str
    routing: Optional[str] = None
    metadata: Optional[Dict] = None

    @classmethod
    def from_backend(cls, backend_res: Dict):
        """
        Normalize backend output into internal typed structure.

        Expected format:
            {
                "labels": [...],
                "scores": [...],
                "meta": {"routing": "chat"}
            }
        """
        labels = backend_res.get("labels", [])
        scores = backend_res.get("scores", [])

        primary = labels[0] if labels else "unknown"
        routing = backend_res.get("meta", {}).get("routing")

        return cls(
            labels=labels,
            scores=scores,
            primary_label=primary,
            routing=routing,
            metadata=backend_res.get("meta", {})
        )
