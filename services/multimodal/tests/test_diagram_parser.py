"""
Unit tests for DiagramParser module using pytest.
"""

import pytest
import os
from pathlib import Path
from diagram_parser import DiagramParser


def test_parse_returns_list(tmp_path):
    """Test that parse returns a list for valid image file."""
    # Create a temporary dummy image file
    dummy_image = tmp_path / "dummy.png"
    dummy_image.write_text("dummy image content")

    parser = DiagramParser()
    result = parser.parse(str(dummy_image))

    assert isinstance(result, list)
    assert len(result) > 0
    assert "diagram_element_placeholder" in result


def test_parse_file_not_found():
    """Test that parse raises FileNotFoundError for non-existent file."""
    parser = DiagramParser()

    with pytest.raises(FileNotFoundError) as excinfo:
        parser.parse("nonexistent.png")

    assert "Image not found" in str(excinfo.value)


def test_health_check():
    """Test DiagramParser health check functionality."""
    parser = DiagramParser()
    health = parser.health_check()

    assert health["module"] == "DiagramParser"
    assert health["status"] == "initialized"
    assert isinstance(health, dict)


def test_parse_with_different_formats(tmp_path):
    """Test parsing with different image formats."""
    formats = ["png", "jpg", "jpeg", "gif", "bmp"]
    parser = DiagramParser()

    for fmt in formats:
        image_file = tmp_path / f"test_image.{fmt}"
        image_file.write_text(f"dummy {fmt} content")

        result = parser.parse(str(image_file))
        assert isinstance(result, list)


def test_parse_with_empty_file(tmp_path):
    """Test parsing an empty image file."""
    empty_image = tmp_path / "empty.png"
    empty_image.write_text("")

    parser = DiagramParser()
    result = parser.parse(str(empty_image))

    # Should either return empty list or handle gracefully
    assert isinstance(result, list)


def test_parse_with_pathlib_path(tmp_path):
    """Test that parse accepts pathlib.Path objects."""
    dummy_image = tmp_path / "pathlib_test.png"
    dummy_image.write_text("dummy content")

    parser = DiagramParser()
    result = parser.parse(dummy_image)  # Pass Path object directly

    assert isinstance(result, list)


def test_parse_result_structure(tmp_path):
    """Test that parse result has expected structure."""
    dummy_image = tmp_path / "structure_test.png"
    dummy_image.write_text("dummy content")

    parser = DiagramParser()
    result = parser.parse(str(dummy_image))

    assert isinstance(result, list)
    # Each element should be a string or dict
    for element in result:
        assert isinstance(element, (str, dict))


def test_parse_with_absolute_path(tmp_path):
    """Test parsing with absolute file path."""
    dummy_image = tmp_path / "absolute_test.png"
    dummy_image.write_text("dummy content")

    parser = DiagramParser()
    absolute_path = str(dummy_image.absolute())
    result = parser.parse(absolute_path)

    assert isinstance(result, list)


def test_parse_with_relative_path(tmp_path):
    """Test parsing with relative file path."""
    # Change to tmp directory
    original_dir = os.getcwd()
    os.chdir(tmp_path)

    try:
        dummy_image = Path("relative_test.png")
        dummy_image.write_text("dummy content")

        parser = DiagramParser()
        result = parser.parse("relative_test.png")

        assert isinstance(result, list)
    finally:
        os.chdir(original_dir)


def test_parse_with_special_characters_in_filename(tmp_path):
    """Test parsing file with special characters in name."""
    special_names = [
        "test-diagram.png",
        "test_diagram.png",
        "test diagram.png",
        "test(1).png"
    ]

    parser = DiagramParser()

    for name in special_names:
        image_file = tmp_path / name
        image_file.write_text("dummy content")

        result = parser.parse(str(image_file))
        assert isinstance(result, list)


def test_parse_multiple_times(tmp_path):
    """Test parsing the same file multiple times."""
    dummy_image = tmp_path / "multi_test.png"
    dummy_image.write_text("dummy content")

    parser = DiagramParser()

    result1 = parser.parse(str(dummy_image))
    result2 = parser.parse(str(dummy_image))
    result3 = parser.parse(str(dummy_image))

    # All results should be lists
    assert isinstance(result1, list)
    assert isinstance(result2, list)
    assert isinstance(result3, list)


def test_parse_different_files_sequentially(tmp_path):
    """Test parsing different files in sequence."""
    parser = DiagramParser()

    for i in range(3):
        image_file = tmp_path / f"test_{i}.png"
        image_file.write_text(f"content {i}")

        result = parser.parse(str(image_file))
        assert isinstance(result, list)


def test_parser_initialization():
    """Test DiagramParser initialization."""
    parser = DiagramParser()

    assert parser is not None
    assert hasattr(parser, 'parse')
    assert hasattr(parser, 'health_check')


def test_parse_with_directory_path(tmp_path):
    """Test that parse handles directory path appropriately."""
    parser = DiagramParser()

    # Pass a directory instead of a file
    with pytest.raises((FileNotFoundError, IsADirectoryError, OSError)):
        parser.parse(str(tmp_path))


def test_parse_with_none_path():
    """Test that parse handles None path appropriately."""
    parser = DiagramParser()

    with pytest.raises((TypeError, ValueError, FileNotFoundError)):
        parser.parse(None)


def test_parse_with_empty_string():
    """Test that parse handles empty string path."""
    parser = DiagramParser()

    with pytest.raises((FileNotFoundError, ValueError)):
        parser.parse("")


def test_parse_large_file(tmp_path):
    """Test parsing a larger file."""
    large_image = tmp_path / "large.png"
    # Create a larger dummy file
    large_image.write_text("x" * 10000)

    parser = DiagramParser()
    result = parser.parse(str(large_image))

    assert isinstance(result, list)


@pytest.fixture
def parser():
    """Fixture to provide a DiagramParser instance."""
    return DiagramParser()


def test_with_fixture(parser, tmp_path):
    """Example test using pytest fixture."""
    dummy_image = tmp_path / "fixture_test.png"
    dummy_image.write_text("dummy content")

    result = parser.parse(str(dummy_image))
    assert isinstance(result, list)


@pytest.mark.parametrize("extension", ["png", "jpg", "jpeg", "gif", "bmp", "tiff"])
def test_various_image_extensions(tmp_path, extension):
    """Test parsing files with various image extensions."""
    image_file = tmp_path / f"test.{extension}"
    image_file.write_text("dummy content")

    parser = DiagramParser()
    result = parser.parse(str(image_file))

    assert isinstance(result, list)


def test_parse_preserves_file(tmp_path):
    """Test that parse doesn't modify the original file."""
    dummy_image = tmp_path / "preserve_test.png"
    original_content = "original content"
    dummy_image.write_text(original_content)

    parser = DiagramParser()
    parser.parse(str(dummy_image))

    # File should still exist and have same content
    assert dummy_image.exists()
    assert dummy_image.read_text() == original_content