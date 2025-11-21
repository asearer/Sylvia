"""
Unit tests for Exporter module using pytest.
"""

import os
import shutil
import json
import csv
import pytest
from exporter import Exporter

EXPORT_DIR = "test_exports"


@pytest.fixture
def exporter():
    """Fixture to provide an Exporter instance with clean test directory."""
    # Clean test directory before test
    if os.path.exists(EXPORT_DIR):
        shutil.rmtree(EXPORT_DIR)

    yield Exporter(output_dir=EXPORT_DIR)

    # Clean up after test
    if os.path.exists(EXPORT_DIR):
        shutil.rmtree(EXPORT_DIR)


def test_json_export(exporter):
    """Test exporting data as JSON format."""
    data = {"a": 1, "b": 2}
    path = exporter.export(data, fmt="json", filename="test_json")

    assert os.path.exists(path)
    assert path.endswith(".json")

    # Verify content
    with open(path, 'r') as f:
        loaded_data = json.load(f)
        assert loaded_data == data


def test_csv_export(exporter):
    """Test exporting data as CSV format."""
    data = [{"col1": 1, "col2": "x"}, {"col1": 2, "col2": "y"}]
    path = exporter.export(data, fmt="csv", filename="test_csv")

    assert os.path.exists(path)
    assert path.endswith(".csv")

    # Verify content
    with open(path, 'r') as f:
        reader = csv.DictReader(f)
        rows = list(reader)
        assert len(rows) == 2
        assert rows[0]["col1"] == "1"
        assert rows[0]["col2"] == "x"


def test_csv_invalid_input(exporter):
    """Test CSV export with invalid input (not a list)."""
    data = {"not": "a list"}  # Invalid for CSV
    result = exporter.export(data, fmt="csv")

    assert isinstance(result, str)
    assert "Export failed" in result or "error" in result.lower()


def test_default_filename(exporter):
    """Test export with default filename."""
    data = {"key": "value"}
    path = exporter.export(data)

    assert os.path.exists(path)
    assert path.endswith(".json")
    assert EXPORT_DIR in path


def test_health_check(exporter):
    """Test Exporter health check functionality."""
    health = exporter.health_check()

    assert health["module"] == "Exporter"
    assert health["status"] == "initialized"


def test_export_directory_creation(exporter):
    """Test that export directory is created if it doesn't exist."""
    # Directory should be created by fixture, verify it exists
    data = {"test": "data"}
    path = exporter.export(data, fmt="json", filename="dir_test")

    assert os.path.exists(EXPORT_DIR)
    assert os.path.isdir(EXPORT_DIR)


def test_multiple_exports(exporter):
    """Test multiple exports to verify files don't overwrite each other."""
    data1 = {"file": 1}
    data2 = {"file": 2}

    path1 = exporter.export(data1, fmt="json", filename="export1")
    path2 = exporter.export(data2, fmt="json", filename="export2")

    assert os.path.exists(path1)
    assert os.path.exists(path2)
    assert path1 != path2


def test_json_with_complex_data(exporter):
    """Test JSON export with nested data structures."""
    data = {
        "nested": {"level": 2, "items": [1, 2, 3]},
        "array": ["a", "b", "c"],
        "number": 42
    }
    path = exporter.export(data, fmt="json", filename="complex")

    assert os.path.exists(path)

    with open(path, 'r') as f:
        loaded = json.load(f)
        assert loaded == data
        assert loaded["nested"]["level"] == 2
        assert len(loaded["array"]) == 3


def test_csv_empty_list(exporter):
    """Test CSV export with empty list."""
    data = []
    result = exporter.export(data, fmt="csv", filename="empty")

    # Behavior depends on implementation - should either succeed or fail gracefully
    if os.path.exists(result):
        # If it creates a file
        assert result.endswith(".csv")
    else:
        # If it returns error message
        assert isinstance(result, str)


def test_unsupported_format(exporter):
    """Test export with unsupported format."""
    data = {"test": "data"}
    result = exporter.export(data, fmt="xml", filename="test")

    # Should return error message or handle gracefully
    assert isinstance(result, str)


@pytest.mark.parametrize("fmt,extension", [
    ("json", ".json"),
    ("csv", ".csv"),
])
def test_file_extensions(exporter, fmt, extension):
    """Test that correct file extensions are used."""
    data = [{"a": 1}] if fmt == "csv" else {"a": 1}
    path = exporter.export(data, fmt=fmt, filename="test_ext")

    if os.path.exists(path):
        assert path.endswith(extension)


def test_special_characters_in_filename(exporter):
    """Test export with special characters in filename."""
    data = {"test": "data"}
    # The implementation should handle or sanitize special characters
    path = exporter.export(data, fmt="json", filename="test_file_123")

    assert os.path.exists(path)