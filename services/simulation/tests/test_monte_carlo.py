import pytest
from monte_carlo import MonteCarlo

def test_monte_carlo_basic():
    mc = MonteCarlo()
    result = mc.simulate(lambda: 1, 5)
    assert len(result) == 5
    assert all(r == 1 for r in result)

def test_monte_carlo_random_values():
    mc = MonteCarlo(seed=42)
    result1 = mc.simulate(lambda: 0.5 + 0.5, 3)
    result2 = mc.simulate(lambda: 0.5 + 0.5, 3)
    assert result1 == result2  # reproducible with same seed

def test_monte_carlo_summary():
    mc = MonteCarlo()
    result = mc.simulate(lambda: 2, 10)
    summary = mc.summarize(result)
    assert summary["mean"] == 2
    assert summary["variance"] == 0
    assert summary["min"] == 2
    assert summary["max"] == 2

def test_monte_carlo_invalid_iterations():
    mc = MonteCarlo()
    with pytest.raises(ValueError):
        mc.simulate(lambda: 1, 0)
