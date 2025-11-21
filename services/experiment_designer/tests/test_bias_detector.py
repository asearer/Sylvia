"""
Unit tests for BiasDetector module using pytest.
"""

import pytest
from bias_detector import BiasDetector


def test_empty_data():
    """Test BiasDetector with empty data."""
    bd = BiasDetector()
    result = bd.detect([])
    assert result["bias_detected"] is False
    assert "No data provided" in result["details"]


def test_small_group_detection():
    """Test detection of groups smaller than minimum size."""
    bd = BiasDetector(min_group_size=2)
    data = [
        {"group": "A", "value": 1},
    ]
    result = bd.detect(data)
    assert result["bias_detected"] is True
    assert "small_groups" in result["details"]


def test_numeric_imbalance():
    """Test detection of numeric value imbalance between groups."""
    bd = BiasDetector(p_threshold=0.5)  # loose threshold to trigger detection
    data = [
        {"group": "A", "value": 1},
        {"group": "A", "value": 2},
        {"group": "B", "value": 10},
        {"group": "B", "value": 12},
    ]
    result = bd.detect(data)
    assert result["bias_detected"] is True
    assert "numeric_imbalance" in result["details"]


def test_categorical_imbalance():
    """Test detection of categorical distribution imbalance."""
    bd = BiasDetector(p_threshold=0.5)
    data = [
        {"group": "A", "category": "X"},
        {"group": "A", "category": "Y"},
        {"group": "B", "category": "Y"},
        {"group": "B", "category": "Y"},
    ]
    result = bd.detect(data)
    assert result["bias_detected"] is True
    assert "categorical_imbalance" in result["details"]


def test_health_check():
    """Test BiasDetector health check functionality."""
    bd = BiasDetector()
    health = bd.health_check()
    assert health["module"] == "BiasDetector"
    assert health["status"] == "initialized"


def test_no_bias_detected():
    """Test case where no bias should be detected."""
    bd = BiasDetector()
    data = [
        {"group": "A", "value": 5},
        {"group": "A", "value": 6},
        {"group": "B", "value": 5},
        {"group": "B", "value": 6},
    ]
    result = bd.detect(data)
    assert result["bias_detected"] is False


def test_multiple_groups():
    """Test with more than two groups."""
    bd = BiasDetector()
    data = [
        {"group": "A", "value": 1},
        {"group": "B", "value": 2},
        {"group": "C", "value": 3},
    ]
    result = bd.detect(data)
    assert "bias_detected" in result
    assert isinstance(result["details"], (str, dict, list))


@pytest.fixture
def bias_detector():
    """Fixture to provide a BiasDetector instance."""
    return BiasDetector()


def test_with_fixture(bias_detector):
    """Example test using pytest fixture."""
    result = bias_detector.detect([])
    assert result["bias_detected"] is False