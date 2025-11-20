"""
Entrypoint for the Simulation service.
Coordinates different simulation engines.
"""

from ode_solver import ODESolver
from pde_solver import PDESolver
from monte_carlo import MonteCarlo
from stochastic_models import StochasticModel
from sweep_engine import SweepEngine

class SimulationService:
    def __init__(self):
        self.ode_solver = ODESolver()
        self.pde_solver = PDESolver()
        self.mc_sim = MonteCarlo()
        self.stochastic = StochasticModel()
        self.sweep_engine = SweepEngine()

    # --- ODE ---
    def run_ode(self, equation, t_span, y0=0.0, num_points=100):
        return self.ode_solver.solve(equation, t_span, y0=y0, num_points=num_points)

    # --- PDE ---
    def run_pde(self, pde, domain, nx=10, nt=10):
        return self.pde_solver.solve(pde, domain, nx=nx, nt=nt)

    # --- Monte Carlo ---
    def run_monte_carlo(self, model, iterations=100):
        return self.mc_sim.simulate(model, iterations)

    # --- Stochastic ---
    def run_stochastic(self, model, params, iterations=100):
        return self.stochastic.simulate(model, params, iterations)

    # --- Parameter Sweep ---
    def run_sweep(self, simulation_func, param_grid, parallel=False, max_workers=None):
        self.sweep_engine.parallel = parallel
        self.sweep_engine.max_workers = max_workers
        return self.sweep_engine.run(simulation_func, param_grid)


if __name__ == "__main__":
    sim = SimulationService()

    # Example ODE
    print("ODE Example:")
    try:
        # dx/dt = -x as a lambda function
        ode_result = sim.run_ode(lambda t, x: -x, (0, 10))
        print(ode_result[:5], "...")  # Print first 5 points
    except Exception as e:
        print(f"ODE failed: {e}")

    # Example Monte Carlo
    print("\nMonte Carlo Example:")
    mc_result = sim.run_monte_carlo(lambda: 2 + 3 * 0.5, iterations=5)
    print(mc_result)

    # Example Stochastic
    print("\nStochastic Example:")
    stochastic_result = sim.run_stochastic(lambda rate: rate * 0.9, {"rate": 10}, iterations=5)
    print(stochastic_result)

    # Example Parameter Sweep
    print("\nSweep Example:")
    sweep_result = sim.run_sweep(lambda a, b: a + b, [{"a": 1, "b": 2}, {"a": 3, "b": 4}])
    print(sweep_result)
