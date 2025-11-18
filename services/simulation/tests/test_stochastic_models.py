from stochastic_models import StochasticModel

def test_stochastic_model():
    sm = StochasticModel()
    result = sm.simulate(lambda x: x**2, {"x":2})
    assert isinstance(result, list)
