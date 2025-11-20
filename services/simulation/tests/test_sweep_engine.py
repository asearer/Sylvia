import pytest
from sweep_engine import SweepEngine

def test_sweep_basic():
    se = SweepEngine()
    result = se.run(lambda x: x*2, [{"x":1}, {"x":2}])
    assert result == [2, 4]

def test_sweep_parallel():
    se = SweepEngine(parallel=True)
    result = se.run(lambda x: x*3, [{"x":1}, {"x":2}, {"x":3}])
    assert result == [3, 6, 9]

def test_sweep_empty_grid():
    se = SweepEngine()
    with pytest.raises(ValueError):
        se.run(lambda x: x, [])

def test_sweep_summary():
    se = SweepEngine()
    results = se.run(lambda x: x*2, [{"x":1}, {"x":2}, {"x":3}])
    summary = se.summarize(results)
    assert summary["mean"] == 4
    assert summary["min"] == 2
    assert summary["max"] == 6
    assert summary["variance"] == pytest.approx(4.0)

def test_sweep_non_numeric():
    se = SweepEngine()
    result = se.run(lambda s: s.upper(), [{"s":"a"}, {"s":"b"}])
    assert result == ["A", "B"]
