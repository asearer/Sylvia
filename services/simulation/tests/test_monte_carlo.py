from monte_carlo import MonteCarlo

def test_monte_carlo():
    mc = MonteCarlo()
    result = mc.simulate(lambda: 1, 5)
    assert len(result) == 5
