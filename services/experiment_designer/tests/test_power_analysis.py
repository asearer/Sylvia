"""
Unit tests for PowerAnalyzer module using pytest.
"""

import pytest
from power_analyzer import PowerAnalyzer


def test_ttest_power():
    """Test power computation for t-test."""
    pa = PowerAnalyzer(alpha=0.05)
    data = {"type": "t-test", "n": 30, "effect_size": 0.5}
    result = pa.compute(data)

    assert "power" in result
    assert result["method"] == "t-test"
    assert result["n"] == 30
    assert 0.0 <= result["power"] <= 1.0


def test_anova_power():
    """Test power computation for ANOVA."""
    pa = PowerAnalyzer(alpha=0.05)
    data = {"type": "anova", "n": 20, "groups": 3, "effect_size": 0.25}
    result = pa.compute(data)

    assert "power" in result
    assert result["method"] == "anova"
    assert result["groups"] == 3
    assert 0.0 <= result["power"] <= 1.0


def test_invalid_test_type():
    """Test handling of unsupported test type."""
    pa = PowerAnalyzer()
    data = {"type": "unsupported"}
    result = pa.compute(data)

    assert "error" in result
    assert result["power"] is None


def test_edge_case_zero_effect():
    """Test power computation with zero effect size."""
    pa = PowerAnalyzer()
    data = {"type": "t-test", "n": 30, "effect_size": 0.0}
    result = pa.compute(data)

    assert "power" in result
    assert result["power"] >= 0.0
    assert result["power"] <= 1.0
    # Zero effect should give power approximately equal to alpha
    assert result["power"] <= 0.1  # Should be close to alpha


def test_health_check():
    """Test PowerAnalyzer health check functionality."""
    pa = PowerAnalyzer()
    health = pa.health_check()

    assert health["module"] == "PowerAnalyzer"
    assert health["status"] == "initialized"


def test_large_effect_size():
    """Test power computation with large effect size."""
    pa = PowerAnalyzer(alpha=0.05)
    data = {"type": "t-test", "n": 30, "effect_size": 0.8}
    result = pa.compute(data)

    assert "power" in result
    # Large effect size should yield high power
    assert result["power"] > 0.5


def test_small_sample_size():
    """Test power computation with small sample size."""
    pa = PowerAnalyzer(alpha=0.05)
    data = {"type": "t-test", "n": 5, "effect_size": 0.5}
    result = pa.compute(data)

    assert "power" in result
    # Small sample should yield lower power
    assert 0.0 <= result["power"] <= 1.0


def test_large_sample_size():
    """Test power computation with large sample size."""
    pa = PowerAnalyzer(alpha=0.05)
    data = {"type": "t-test", "n": 1000, "effect_size": 0.5}
    result = pa.compute(data)

    assert "power" in result
    # Large sample should yield high power
    assert result["power"] > 0.8


def test_different_alpha_levels():
    """Test power computation with different alpha levels."""
    pa_strict = PowerAnalyzer(alpha=0.01)
    pa_lenient = PowerAnalyzer(alpha=0.10)

    data = {"type": "t-test", "n": 30, "effect_size": 0.5}

    result_strict = pa_strict.compute(data)
    result_lenient = pa_lenient.compute(data)

    # More lenient alpha should give higher power
    assert result_lenient["power"] >= result_strict["power"]


def test_anova_multiple_groups():
    """Test ANOVA with varying number of groups."""
    pa = PowerAnalyzer(alpha=0.05)

    data_2groups = {"type": "anova", "n": 20, "groups": 2, "effect_size": 0.25}
    data_5groups = {"type": "anova", "n": 20, "groups": 5, "effect_size": 0.25}

    result_2 = pa.compute(data_2groups)
    result_5 = pa.compute(data_5groups)

    assert "power" in result_2
    assert "power" in result_5
    assert 0.0 <= result_2["power"] <= 1.0
    assert 0.0 <= result_5["power"] <= 1.0


def test_missing_parameters():
    """Test handling of missing required parameters."""
    pa = PowerAnalyzer()
    data = {"type": "t-test", "n": 30}  # Missing effect_size
    result = pa.compute(data)

    # Should either handle gracefully or return error
    assert "error" in result or "power" in result


def test_negative_parameters():
    """Test handling of invalid negative parameters."""
    pa = PowerAnalyzer()
    data = {"type": "t-test", "n": -10, "effect_size": 0.5}
    result = pa.compute(data)

    # Should return error for invalid parameters
    assert "error" in result or result["power"] is None


def test_result_structure():
    """Test that result has expected structure."""
    pa = PowerAnalyzer(alpha=0.05)
    data = {"type": "t-test", "n": 30, "effect_size": 0.5}
    result = pa.compute(data)

    assert isinstance(result, dict)
    assert "power" in result or "error" in result
    assert "method" in result


@pytest.fixture
def power_analyzer():
    """Fixture to provide a PowerAnalyzer instance."""
    return PowerAnalyzer(alpha=0.05)


def test_with_fixture(power_analyzer):
    """Example test using pytest fixture."""
    data = {"type": "t-test", "n": 30, "effect_size": 0.5}
    result = power_analyzer.compute(data)
    assert "power" in result


@pytest.mark.parametrize("test_type,params", [
    ("t-test", {"n": 30, "effect_size": 0.5}),
    ("t-test", {"n": 50, "effect_size": 0.3}),
    ("anova", {"n": 20, "groups": 3, "effect_size": 0.25}),
    ("anova", {"n": 40, "groups": 4, "effect_size": 0.4}),
])
def test_various_configurations(test_type, params):
    """Test various test configurations using parametrize."""
    pa = PowerAnalyzer(alpha=0.05)
    data = {"type": test_type, **params}
    result = pa.compute(data)

    assert "power" in result or "error" in result
    if "power" in result and result["power"] is not None:
        assert 0.0 <= result["power"] <= 1.0


def test_power_increases_with_sample_size():
    """Test that power increases as sample size increases."""
    pa = PowerAnalyzer(alpha=0.05)

    result_small = pa.compute({"type": "t-test", "n": 10, "effect_size": 0.5})
    result_large = pa.compute({"type": "t-test", "n": 100, "effect_size": 0.5})

    if "power" in result_small and "power" in result_large:
        assert result_large["power"] >= result_small["power"]