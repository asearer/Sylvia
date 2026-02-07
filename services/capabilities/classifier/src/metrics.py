# classifier/src/metrics.py
"""
Utility for tracking ML training metrics.
"""

from dataclasses import dataclass


@dataclass
class MetricState:
    epoch: int
    loss: float
    accuracy: float
