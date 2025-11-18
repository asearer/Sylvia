from main import SimulationService

def test_simulation_service():
    sim = SimulationService()
    result = sim.run_ode("dx/dt=-x", (0,1))
    assert isinstance(result, list)
