import pytest
from pde_solver import PDESolver


def test_pde_solver_basic():
    solver = PDESolver()

    # Simple PDE: du/dt = -u (decay) for each spatial point
    def pde(t, x, u):
        return -u

    domain = {
        "x_start": 0,
        "x_end": 1,
        "t_start": 0,
        "t_end": 1
    }

    result = solver.solve(pde, domain, nx=5, nt=5)
    assert isinstance(result, list)
    assert len(result) == 5  # number of time points
    for row in result:
        assert isinstance(row, list)
        assert len(row) == 5  # number of spatial points


def test_pde_solver_boundary_conditions():
    solver = PDESolver()

    def pde(t, x, u):
        return 1  # constant growth

    domain = {"x_start": 0, "x_end": 1, "t_start": 0, "t_end": 1}
    result = solver.solve(pde, domain, nx=3, nt=3)

    # Check Dirichlet boundaries are zero
    for row in result:
        assert row[0] == 0
        assert row[-1] == 0


def test_pde_solver_missing_domain_keys():
    solver = PDESolver()

    def pde(t, x, u): return u

    # Missing keys
    domain = {"x_start": 0, "x_end": 1, "t_start": 0}
    with pytest.raises(ValueError):
        solver.solve(pde, domain)


def test_pde_solver_invalid_domain():
    solver = PDESolver()

    def pde(t, x, u): return u

    domain = {"x_start": 1, "x_end": 0, "t_start": 0, "t_end": 1}
    with pytest.raises(ValueError):
        solver.solve(pde, domain)
