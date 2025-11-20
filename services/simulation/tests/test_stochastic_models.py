import pytest
from stochastic_models import StochasticModel

def test_stochastic_basic():
    sm = StochasticModel(seed=42)
    result = sm.simulate(lambda x: x**2, {"x": 2}, iterations=5)
    assert isinstance(result, list)
    assert len(result) == 5
    assert all(r == 4 for r in result)

def test_stochastic_different_values():
    sm = StochasticModel()
    import random
    # Stochastic model: return random int
    result = sm.simulate(lambda seed=None: random.randint(0,10), {}, iterations=10)
    assert all(isinstance(r, int) for r in result)

def test_stochastic_summary():
    sm = StochasticModel()
    result = sm.simulate(lambda x: x**2, {"x":3}, iterations=5)
    summary = sm.summarize(result)
    assert summary["mean"] == 9
    assert summary["variance"] == 0
    assert summary["min"] == 9
    assert summary["max"] == 9

def test_stochastic_invalid_iterations():
    sm = StochasticModel()
    with pytest.raises(ValueError):
        sm.simulate(lambda x: x, {"x":1}, iterations=0)

def test_stochastic_empty_summary():
    sm = StochasticModel()
    with pytest.raises(ValueError):
        sm.summarize([])
