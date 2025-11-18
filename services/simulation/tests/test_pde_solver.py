from pde_solver import PDESolver

def test_pde_solver():
    solver = PDESolver()
    result = solver.solve("d2u/dx2 = du/dt", {"x":10, "t":5})
    assert isinstance(result, list)
