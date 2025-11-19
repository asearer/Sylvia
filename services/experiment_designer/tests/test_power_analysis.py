import pytest
from power_analyzer import PowerAnalyzer

def test_ttest_power():
    pa = PowerAnalyzer(alpha=0.05)
    data = {"type": "t-test", "n": 30, "effect_size": 0.5}
    result = pa.compute(data)
    assert "power" in result
    assert result["method"] == "t-test"
    assert result["n"] == 30

def test_anova_power():
    pa = PowerAnalyzer(alpha=0.05)
    data = {"type": "anova", "n": 20, "groups": 3, "effect_size": 0.25}
    result = pa.compute(data)
    assert "power" in result
    assert result["method"] == "anova"
    assert result["groups"] == 3

def test_invalid_test_type():
    pa = PowerAnalyzer()
    data = {"type": "unsupported"}
    result = pa.compute(data)
    assert "error" in result
    assert result["power"] is None

def test_edge_case_zero_effect():
    pa = PowerAnalyzer()
    data = {"type": "t-test", "n": 30, "effect_size": 0.0}
    result = pa.compute(data)
    assert result["power"] >= 0.0
    assert result["power"] <= 1.0

def test_health_check():
    pa = PowerAnalyzer()
    health = pa.health_check()
    assert health["module"] == "PowerAnalyzer"
    assert health["status"] == "initialized"
