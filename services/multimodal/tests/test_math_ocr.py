import pytest
from math_ocr import MathOCR

def test_extract_returns_placeholder(tmp_path):
    # Create a temporary dummy image file
    dummy_image = tmp_path / "dummy.png"
    dummy_image.write_text("dummy content")

    ocr = MathOCR()
    math_text = ocr.extract(str(dummy_image))
    assert isinstance(math_text, str)
    assert "placeholder" in math_text

def test_extract_file_not_found():
    ocr = MathOCR()
    with pytest.raises(FileNotFoundError):
        ocr.extract("nonexistent.png")

def test_health_check():
    ocr = MathOCR()
    health = ocr.health_check()
    assert health["module"] == "MathOCR"
    assert health["status"] == "initialized"
