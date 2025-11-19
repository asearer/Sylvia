import os
import shutil
import pytest
from main import ExperimentDesigner

EXPORT_DIR = "test_exports"

@pytest.fixture
def ed():
    # Clean exports dir
    if os.path.exists(EXPORT_DIR):
        shutil.rmtree(EXPORT_DIR)
    exp_designer = ExperimentDesigner()
    exp_designer.exporter.output_dir = EXPORT_DIR
    return exp_designer

def test_create_experiment(ed):
    params = {"factors": 2, "levels": 3, "replicates": 2}
    exp = ed.create_experiment(params)
    assert "design" in exp
    assert exp["parameters"] == params

def test_analyze_experiment(ed):
    dummy_data = [
        {"group": "control", "value": 1},
        {"group": "treatment", "value": 2},
    ]
    analysis = ed.analyze_experiment(dummy_data)
    assert "power" in analysis
    assert "bias" in analysis

def test_export_json(ed):
    experiment = {"design": "test", "parameters": {"factors": 1}}
    path = ed.export(experiment, fmt="json")
    assert os.path.exists(path)
    assert path.endswith(".json")

def test_export_csv(ed):
    experiment = [{"col1": 1, "col2": 2}, {"col1": 3, "col2": 4}]
    path = ed.export(experiment, fmt="csv")
    assert os.path.exists(path)
    assert path.endswith(".csv")

def test_health_checks(ed):
    health_gen = ed.generator.health_check()
    health_power = ed.power_analyzer.health_check()
    health_bias = ed.bias_detector.health_check()
    health_export = ed.exporter.health_check()
    assert health_gen["status"] == "initialized"
    assert health_power["status"] == "initialized"
    assert health_bias["status"] == "initialized"
    assert health_export["status"] == "initialized"

def test_edge_case_empty_parameters(ed):
    exp = ed.create_experiment({})
    assert "design" in exp
    analysis = ed.analyze_experiment([])
    assert "power" in analysis
    assert "bias" in analysis
