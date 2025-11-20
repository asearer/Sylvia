"""
Stochastic simulation engine.
"""

from typing import Callable, Dict, List, Optional
import random
import statistics

class StochasticModel:
    def __init__(self, seed: Optional[int] = None):
        """
        Initialize stochastic simulation engine.

        Args:
            seed (int, optional): Random seed for reproducibility.
        """
        if seed is not None:
            random.seed(seed)

    def simulate(
        self,
        model: Callable[..., float],
        params: Dict,
        iterations: int = 100
    ) -> List[float]:
        """
        Simulate stochastic system.

        Args:
            model (callable): Stochastic model function.
            params (dict): Parameters for simulation.
            iterations (int): Number of simulation runs.

        Returns:
            list: Simulation results.
        """
        if iterations <= 0:
            raise ValueError("Iterations must be a positive integer.")

        results = [model(**params) for _ in range(iterations)]
        return results

    def summarize(self, results: List[float]) -> Dict[str, float]:
        """
        Return summary statistics for simulation results.

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
