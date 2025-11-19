import os
import shutil
import pytest
from exporter import Exporter

EXPORT_DIR = "test_exports"

@pytest.fixture
def exporter():
    # Clean test directory
    if os.path.exists(EXPORT_DIR):
        shutil.rmtree(EXPORT_DIR)
    return Exporter(output_dir=EXPORT_DIR)

def test_json_export(exporter):
    data = {"a": 1, "b": 2}
    path = exporter.export(data, fmt="json", filename="test_json")
    assert os.path.exists(path)
    assert path.endswith(".json")

def test_csv_export(exporter):
    data = [{"col1": 1, "col2": "x"}, {"col1": 2, "col2": "y"}]
    path = exporter.export(data, fmt="csv", filename="test_csv")
    assert os.path.exists(path)
    assert path.endswith(".csv")

def test_csv_invalid_input(exporter):
    data = {"not": "a list"}  # Invalid for CSV
    result = exporter.export(data, fmt="csv")
    assert "Export failed" in result

def test_default_filename(exporter):
    data = {"key": "value"}
    path = exporter.export(data)
    assert os.path.exists(path)
    assert path.endswith(".json")

def test_health_check(exporter):
    health = exporter.health_check()
    assert health["module"] == "Exporter"
    assert health["status"] == "initialized"
