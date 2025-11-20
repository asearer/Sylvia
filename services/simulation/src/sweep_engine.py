"""
Runs parameter sweeps over simulation functions.
"""

from typing import Callable, List, Dict, Optional
import statistics
from concurrent.futures import ThreadPoolExecutor

class SweepEngine:
    def __init__(self, parallel: bool = False, max_workers: Optional[int] = None):
        """
        Initialize the Sweep Engine.

        Args:
            parallel (bool): Run sweep in parallel if True.
            max_workers (int, optional): Number of threads for parallel execution.
        """
        self.parallel = parallel
        self.max_workers = max_workers

    def run(self, simulation_func: Callable[..., float], param_grid: List[Dict]) -> List[float]:
        """
        Run a sweep over parameter grid.

        Args:
            simulation_func (callable): Simulation function.
            param_grid (list of dicts): List of parameter sets.

        Returns:
            list: Sweep results.
        """
        if not param_grid:
            raise ValueError("Parameter grid is empty.")

        results = []

        if self.parallel:
            with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
                futures = [executor.submit(simulation_func, **params) for params in param_grid]
                results = [f.result() for f in futures]
        else:
            for params in param_grid:
                results.append(simulation_func(**params))

        return results

    def summarize(self, results: List[float]) -> Dict[str, float]:
        """
        Return summary statistics for sweep results.

        Args:
            results (list): List of sweep results.

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
