from sweep_engine import SweepEngine

def test_sweep_engine():
    se = SweepEngine()
    result = se.run(lambda x: x*2, [{"x":1}, {"x":2}])
    assert result == [2, 4]
