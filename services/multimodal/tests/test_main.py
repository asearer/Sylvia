import pytest
from main import MultimodalReasoning


def test_process_image(tmp_path):
    # Create a temporary dummy image file
    dummy_image = tmp_path / "dummy.png"
    dummy_image.write_text("dummy content")

    mm = MultimodalReasoning()
    result = mm.process_image(str(dummy_image))

    # Validate fused output contains all expected keys
    assert isinstance(result, dict)
    assert "diagrams" in result
    assert "math" in result
    assert "tables" in result
    assert "captions" in result


def test_process_image_file_not_found():
    mm = MultimodalReasoning()
    with pytest.raises(FileNotFoundError):
        mm.process_image("nonexistent.png")


def test_health_check():
    mm = MultimodalReasoning()
    health = mm.health_check()
    expected_modules = ["DiagramParser", "MathOCR", "TableExtractor", "ImageCaptioner", "FusionEngine"]

    for module in expected_modules:
        assert module in health
        assert health[module]["status"] == "initialized"
