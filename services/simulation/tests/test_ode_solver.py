from ode_solver import ODESolver

def test_ode_solver():
    solver = ODESolver()
    result = solver.solve("dx/dt = -x", (0,2))
    assert isinstance(result, list)
