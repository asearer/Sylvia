from power_analysis import PowerAnalyzer

def test_power_analysis():
    pa = PowerAnalyzer()
    result = pa.compute([1,2,3])
    assert "power" in result
