"""
Monte Carlo simulation engine.
"""

import random
from typing import Callable, List, Optional, Dict
import statistics

class MonteCarlo:
    def __init__(self, seed: Optional[int] = None):
        """
        Initialize Monte Carlo engine.

        Args:
            seed (int, optional): Random seed for reproducibility.
        """
        if seed is not None:
            random.seed(seed)

    def simulate(self, model: Callable[[], float], iterations: int) -> List[float]:
        """
        Run Monte Carlo simulations.

        Args:
            model (callable): Model function to simulate, returns a float.
            iterations (int): Number of iterations.

        Returns:
            list: Simulation results.
        """
        if iterations <= 0:
            raise ValueError("Iterations must be a positive integer.")

        results = [model() for _ in range(iterations)]
        return results

    def summarize(self, results: List[float]) -> Dict[str, float]:
        """
        Return statistical summary of simulation results.

        Args:
            results (list): List of simulation results.

        Returns:
            dict: Mean, variance, min, max.
        """
        if not results:
            raise ValueError("Results list is empty.")

        return {
            "mean": statistics.mean(results),
            "variance": statistics.variance(results) if len(results) > 1 else 0.0,
            "min": min(results),
            "max": max(results)
        }
