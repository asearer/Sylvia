import pytest
from main import SimulationService

def test_service_ode_lambda():
    sim = SimulationService()
    result = sim.run_ode(lambda t, x: -x, (0,1), y0=1, num_points=5)
    assert isinstance(result, list)
    assert len(result) == 5
    assert result[0][1] == 1

def test_service_ode_string():
    sim = SimulationService()
    result = sim.run_ode("lambda t, x: -x", (0,1), y0=2, num_points=3)
    assert isinstance(result, list)
    assert len(result) == 3
    assert result[0][1] == 2

def test_service_pde():
    sim = SimulationService()
    def pde(t, x, u): return -u
    domain = {"x_start":0, "x_end":1, "t_start":0, "t_end":1}
    result = sim.run_pde(pde, domain, nx=3, nt=3)
    assert isinstance(result, list)
    assert len(result) == 3
    for row in result:
        assert len(row) == 3

def test_service_monte_carlo():
    sim = SimulationService()
    result = sim.run_monte_carlo(lambda: 5, iterations=4)
    assert isinstance(result, list)
    assert all(r == 5 for r in result)

def test_service_stochastic():
    sim = SimulationService()
    result = sim.run_stochastic(lambda x: x**2, {"x":2}, iterations=3)
    assert isinstance(result, list)
    assert all(r == 4 for r in result)

def test_service_sweep():
    sim = SimulationService()
    result = sim.run_sweep(lambda a, b: a+b, [{"a":1,"b":2},{"a":3,"b":4}])
    assert result == [3,7]

def test_service_invalid_ode():
    sim = SimulationService()
    with pytest.raises(ValueError):
        sim.run_ode("invalid eq", (0,1))

def test_service_empty_sweep():
    sim = SimulationService()
    with pytest.raises(ValueError):
        sim.run_sweep(lambda x: x, [])

def test_service_parallel_sweep():
    sim = SimulationService()
    sim.sweep_engine.parallel = True
    result = sim.run_sweep(lambda x: x*2, [{"x":1},{"x":2}])
    assert result == [2,4]
