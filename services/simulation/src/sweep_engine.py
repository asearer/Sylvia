"""
Runs parameter sweeps over simulation functions.
"""

class SweepEngine:
    def run(self, simulation_func, param_grid):
        """
        Run a sweep over parameter grid.

        Args:
            simulation_func (callable): Simulation function.
            param_grid (list[dict]): List of parameter sets.

        Returns:
            list: Sweep results.
        """
        results = []
        for params in param_grid:
            results.append(simulation_func(**params))
        return results
