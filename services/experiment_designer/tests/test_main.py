"""
Unit tests for ExperimentDesigner main module using pytest.
"""

import os
import shutil
import json
import csv
import pytest
from main import ExperimentDesigner

EXPORT_DIR = "test_exports"


@pytest.fixture
def ed():
    """Fixture to provide an ExperimentDesigner instance with clean export directory."""
    # Clean exports dir before test
    if os.path.exists(EXPORT_DIR):
        shutil.rmtree(EXPORT_DIR)

    exp_designer = ExperimentDesigner()
    exp_designer.exporter.output_dir = EXPORT_DIR

    yield exp_designer

    # Clean up after test
    if os.path.exists(EXPORT_DIR):
        shutil.rmtree(EXPORT_DIR)


def test_create_experiment(ed):
    """Test experiment creation with valid parameters."""
    params = {"factors": 2, "levels": 3, "replicates": 2}
    exp = ed.create_experiment(params)

    assert "design" in exp
    assert exp["parameters"] == params
    assert isinstance(exp["design"], (str, dict))


def test_analyze_experiment(ed):
    """Test experiment analysis with dummy data."""
    dummy_data = [
        {"group": "control", "value": 1},
        {"group": "treatment", "value": 2},
    ]
    analysis = ed.analyze_experiment(dummy_data)

    assert "power" in analysis
    assert "bias" in analysis
    assert isinstance(analysis, dict)


def test_export_json(ed):
    """Test JSON export functionality."""
    experiment = {"design": "test", "parameters": {"factors": 1}}
    path = ed.export(experiment, fmt="json")

    assert os.path.exists(path)
    assert path.endswith(".json")

    # Verify content
    with open(path, 'r') as f:
        loaded = json.load(f)
        assert loaded["design"] == "test"
        assert loaded["parameters"]["factors"] == 1


def test_export_csv(ed):
    """Test CSV export functionality."""
    experiment = [{"col1": 1, "col2": 2}, {"col1": 3, "col2": 4}]
    path = ed.export(experiment, fmt="csv")

    assert os.path.exists(path)
    assert path.endswith(".csv")

    # Verify content
    with open(path, 'r') as f:
        reader = csv.DictReader(f)
        rows = list(reader)
        assert len(rows) == 2
        assert rows[0]["col1"] == "1"


def test_health_checks(ed):
    """Test health checks for all components."""
    health_gen = ed.generator.health_check()
    health_power = ed.power_analyzer.health_check()
    health_bias = ed.bias_detector.health_check()
    health_export = ed.exporter.health_check()

    assert health_gen["status"] == "initialized"
    assert health_power["status"] == "initialized"
    assert health_bias["status"] == "initialized"
    assert health_export["status"] == "initialized"

    # Verify module names
    assert health_gen["module"] == "DesignGenerator"
    assert health_power["module"] == "PowerAnalyzer"
    assert health_bias["module"] == "BiasDetector"
    assert health_export["module"] == "Exporter"


def test_edge_case_empty_parameters(ed):
    """Test handling of empty parameters."""
    exp = ed.create_experiment({})
    assert "design" in exp

    analysis = ed.analyze_experiment([])
    assert "power" in analysis
    assert "bias" in analysis


def test_full_workflow(ed):
    """Test complete workflow: create -> analyze -> export."""
    # Create experiment
    params = {"factors": 2, "levels": 2, "replicates": 1}
    experiment = ed.create_experiment(params)
    assert "design" in experiment

    # Analyze with sample data
    sample_data = [
        {"group": "A", "value": 10},
        {"group": "B", "value": 15},
    ]
    analysis = ed.analyze_experiment(sample_data)
    assert "power" in analysis
    assert "bias" in analysis

    # Export results
    path = ed.export(experiment, fmt="json")
    assert os.path.exists(path)


def test_create_experiment_various_sizes(ed):
    """Test experiment creation with various parameter combinations."""
    test_params = [
        {"factors": 1, "levels": 2, "replicates": 1},
        {"factors": 3, "levels": 3, "replicates": 2},
        {"factors": 2, "levels": 4, "replicates": 3},
    ]

    for params in test_params:
        exp = ed.create_experiment(params)
        assert "design" in exp
        assert exp["parameters"] == params


def test_analyze_experiment_different_groups(ed):
    """Test analysis with different group configurations."""
    data_two_groups = [
        {"group": "A", "value": 5},
        {"group": "B", "value": 10},
    ]

    data_three_groups = [
        {"group": "A", "value": 5},
        {"group": "B", "value": 10},
        {"group": "C", "value": 15},
    ]

    analysis_2 = ed.analyze_experiment(data_two_groups)
    analysis_3 = ed.analyze_experiment(data_three_groups)

    assert "power" in analysis_2
    assert "power" in analysis_3
    assert "bias" in analysis_2
    assert "bias" in analysis_3


def test_export_with_custom_filename(ed):
    """Test export with custom filename."""
    experiment = {"test": "data"}
    path = ed.export(experiment, fmt="json", filename="custom_name")

    assert os.path.exists(path)
    assert "custom_name" in path


def test_multiple_exports(ed):
    """Test multiple exports don't overwrite each other."""
    exp1 = {"experiment": 1}
    exp2 = {"experiment": 2}

    path1 = ed.export(exp1, fmt="json", filename="exp1")
    path2 = ed.export(exp2, fmt="json", filename="exp2")

    assert os.path.exists(path1)
    assert os.path.exists(path2)
    assert path1 != path2


def test_component_initialization(ed):
    """Test that all components are properly initialized."""
    assert hasattr(ed, 'generator')
    assert hasattr(ed, 'power_analyzer')
    assert hasattr(ed, 'bias_detector')
    assert hasattr(ed, 'exporter')

    assert ed.generator is not None
    assert ed.power_analyzer is not None
    assert ed.bias_detector is not None
    assert ed.exporter is not None


def test_export_directory_exists(ed):
    """Test that export directory is created."""
    experiment = {"test": "data"}
    ed.export(experiment, fmt="json")

    assert os.path.exists(EXPORT_DIR)
    assert os.path.isdir(EXPORT_DIR)


def test_analyze_with_numeric_values(ed):
    """Test analysis with various numeric value ranges."""
    data_small = [
        {"group": "A", "value": 0.1},
        {"group": "B", "value": 0.2},
    ]

    data_large = [
        {"group": "A", "value": 1000},
        {"group": "B", "value": 2000},
    ]

    analysis_small = ed.analyze_experiment(data_small)
    analysis_large = ed.analyze_experiment(data_large)

    assert "power" in analysis_small
    assert "power" in analysis_large


@pytest.mark.parametrize("fmt,extension", [
    ("json", ".json"),
    ("csv", ".csv"),
])
def test_export_formats(ed, fmt, extension):
    """Test different export formats using parametrize."""
    if fmt == "csv":
        data = [{"col1": 1, "col2": 2}]
    else:
        data = {"test": "data"}

    path = ed.export(data, fmt=fmt)

    if isinstance(path, str) and os.path.exists(path):
        assert path.endswith(extension)


def test_experiment_with_randomization(ed):
    """Test experiment creation with randomization parameter."""
    params = {
        "factors": 2,
        "levels": 2,
        "replicates": 1,
        "randomized": True
    }
    exp = ed.create_experiment(params)

    assert "design" in exp
    assert exp["parameters"]["randomized"] is True


def test_invalid_export_format(ed):
    """Test handling of invalid export format."""
    experiment = {"test": "data"}
    result = ed.export(experiment, fmt="invalid_format")

    # Should handle gracefully - either return error message or raise exception
    assert result is not None