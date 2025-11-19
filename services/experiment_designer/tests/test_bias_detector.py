import pytest
from bias_detector import BiasDetector

def test_empty_data():
    bd = BiasDetector()
    result = bd.detect([])
    assert result["bias_detected"] is False
    assert "No data provided" in result["details"]

def test_small_group_detection():
    bd = BiasDetector(min_group_size=2)
    data = [
        {"group": "A", "value": 1},
    ]
    result = bd.detect(data)
    assert result["bias_detected"] is True
    assert "small_groups" in result["details"]

def test_numeric_imbalance():
    bd = BiasDetector(p_threshold=0.5)  # loose threshold to trigger detection
    data = [
        {"group": "A", "value": 1},
        {"group": "A", "value": 2},
        {"group": "B", "value": 10},
        {"group": "B", "value": 12},
    ]
    result = bd.detect(data)
    assert "numeric_imbalance" in result["details"]

def test_categorical_imbalance():
    bd = BiasDetector(p_threshold=0.5)
    data = [
        {"group": "A", "category": "X"},
        {"group": "A", "category": "Y"},
        {"group": "B", "category": "Y"},
        {"group": "B", "category": "Y"},
    ]
    result = bd.detect(data)
    assert "categorical_imbalance" in result["details"]

def test_health_check():
    bd = BiasDetector()
    health = bd.health_check()
    assert health["module"] == "BiasDetector"
    assert health["status"] == "initialized"
