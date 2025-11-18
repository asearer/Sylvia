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

    def run_ode(self, equation, t_span):
        return self.ode_solver.solve(equation, t_span)

    def run_pde(self, pde, domain):
        return self.pde_solver.solve(pde, domain)

    def run_monte_carlo(self, model, iterations):
        return self.mc_sim.simulate(model, iterations)

    def run_stochastic(self, model, params):
        return self.stochastic.simulate(model, params)

    def run_sweep(self, simulation_func, param_grid):
        return self.sweep_engine.run(simulation_func, param_grid)

if __name__ == "__main__":
    sim = SimulationService()
    print(sim.run_ode("dx/dt = -x", (0,10)))
