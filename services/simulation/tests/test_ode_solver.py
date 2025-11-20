import pytest
from ode_solver import ODESolver

def test_ode_solver_basic_lambda():
    solver = ODESolver()
    result = solver.solve(lambda t, x: -x, (0, 2), y0=1, num_points=5)
    assert isinstance(result, list)
    assert len(result) == 5
    # Check first value equals initial condition
    assert result[0][1] == 1

def test_ode_solver_basic_string():
    solver = ODESolver()
    # Use a lambda string safely
    eq_str = "lambda t, x: -x"
    result = solver.solve(eq_str, (0, 2), y0=2, num_points=4)
    assert isinstance(result, list)
    assert len(result) == 4
    assert result[0][1] == 2

def test_ode_solver_invalid_tspan():
    solver = ODESolver()
    with pytest.raises(ValueError):
        solver.solve(lambda t, x: -x, (2, 0))

def test_ode_solver_invalid_equation():
    solver = ODESolver()
    with pytest.raises(ValueError):
        solver.solve("invalid equation", (0, 2))

def test_ode_solver_callable_output():
    solver = ODESolver()
    result = solver.solve(lambda t, x: -2*x, (0, 1), y0=3, num_points=3)
    # Check tuple format (t, y)
    for t_val, y_val in result:
        assert isinstance(t_val, float)
        assert isinstance(y_val, float)
