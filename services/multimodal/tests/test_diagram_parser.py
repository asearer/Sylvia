import pytest
from diagram_parser import DiagramParser
import os

def test_parse_returns_list(tmp_path):
    # Create a temporary dummy image file
    dummy_image = tmp_path / "dummy.png"
    dummy_image.write_text("dummy image content")

    parser = DiagramParser()
    result = parser.parse(str(dummy_image))
    assert isinstance(result, list)
    assert "diagram_element_placeholder" in result

def test_parse_file_not_found():
    parser = DiagramParser()
    try:
        parser.parse("nonexistent.png")
    except FileNotFoundError as e:
        assert "Image not found" in str(e)

def test_health_check():
    parser = DiagramParser()
    health = parser.health_check()
    assert health["module"] == "DiagramParser"
    assert health["status"] == "initialized"
