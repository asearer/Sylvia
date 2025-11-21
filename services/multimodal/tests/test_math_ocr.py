"""
Unit tests for MathOCR module using pytest.
"""

import pytest
import os
from pathlib import Path
from math_ocr import MathOCR


def test_extract_returns_placeholder(tmp_path):
    """Test that extract returns a string containing placeholder."""
    # Create a temporary dummy image file
    dummy_image = tmp_path / "dummy.png"
    dummy_image.write_text("dummy content")

    ocr = MathOCR()
    math_text = ocr.extract(str(dummy_image))

    assert isinstance(math_text, str)
    assert len(math_text) > 0
    assert "placeholder" in math_text


def test_extract_file_not_found():
    """Test that extract raises FileNotFoundError for non-existent file."""
    ocr = MathOCR()

    with pytest.raises(FileNotFoundError):
        ocr.extract("nonexistent.png")


def test_health_check():
    """Test MathOCR health check functionality."""
    ocr = MathOCR()
    health = ocr.health_check()

    assert health["module"] == "MathOCR"
    assert health["status"] == "initialized"
    assert isinstance(health, dict)


def test_extract_with_different_formats(tmp_path):
    """Test extracting from different image formats."""
    formats = ["png", "jpg", "jpeg", "gif", "bmp"]
    ocr = MathOCR()

    for fmt in formats:
        image_file = tmp_path / f"math_image.{fmt}"
        image_file.write_text(f"dummy {fmt} content")

        math_text = ocr.extract(str(image_file))
        assert isinstance(math_text, str)
        assert len(math_text) > 0


def test_extract_with_empty_file(tmp_path):
    """Test extracting from an empty image file."""
    empty_image = tmp_path / "empty.png"
    empty_image.write_text("")

    ocr = MathOCR()
    math_text = ocr.extract(str(empty_image))

    assert isinstance(math_text, str)


def test_extract_with_pathlib_path(tmp_path):
    """Test that extract accepts pathlib.Path objects."""
    dummy_image = tmp_path / "pathlib_test.png"
    dummy_image.write_text("dummy content")

    ocr = MathOCR()
    math_text = ocr.extract(dummy_image)  # Pass Path object directly

    assert isinstance(math_text, str)


def test_extract_multiple_images(tmp_path):
    """Test extracting from multiple images sequentially."""
    ocr = MathOCR()
    results = []

    for i in range(5):
        image_file = tmp_path / f"math_{i}.png"
        image_file.write_text(f"content {i}")

        math_text = ocr.extract(str(image_file))
        results.append(math_text)
        assert isinstance(math_text, str)

    # All results should be strings
    assert all(isinstance(r, str) for r in results)


def test_extract_same_image_multiple_times(tmp_path):
    """Test extracting from the same image multiple times."""
    dummy_image = tmp_path / "repeat_test.png"
    dummy_image.write_text("dummy content")

    ocr = MathOCR()

    result1 = ocr.extract(str(dummy_image))
    result2 = ocr.extract(str(dummy_image))
    result3 = ocr.extract(str(dummy_image))

    # All should return valid strings
    assert isinstance(result1, str)
    assert isinstance(result2, str)
    assert isinstance(result3, str)


def test_extract_with_absolute_path(tmp_path):
    """Test extracting with absolute file path."""
    dummy_image = tmp_path / "absolute_test.png"
    dummy_image.write_text("dummy content")

    ocr = MathOCR()
    absolute_path = str(dummy_image.absolute())
    math_text = ocr.extract(absolute_path)

    assert isinstance(math_text, str)


def test_extract_with_relative_path(tmp_path):
    """Test extracting with relative file path."""
    original_dir = os.getcwd()
    os.chdir(tmp_path)

    try:
        dummy_image = Path("relative_test.png")
        dummy_image.write_text("dummy content")

        ocr = MathOCR()
        math_text = ocr.extract("relative_test.png")

        assert isinstance(math_text, str)
    finally:
        os.chdir(original_dir)


def test_extract_with_special_characters_in_filename(tmp_path):
    """Test extracting from file with special characters in name."""
    special_names = [
        "math-equation.png",
        "math_equation.png",
        "math equation.png",
        "math(1).png",
        "math[2].png"
    ]

    ocr = MathOCR()

    for name in special_names:
        image_file = tmp_path / name
        image_file.write_text("dummy content")

        math_text = ocr.extract(str(image_file))
        assert isinstance(math_text, str)


def test_extract_with_large_file(tmp_path):
    """Test extracting from a larger file."""
    large_image = tmp_path / "large.png"
    # Create a larger dummy file
    large_image.write_text("x" * 100000)

    ocr = MathOCR()
    math_text = ocr.extract(str(large_image))

    assert isinstance(math_text, str)


def test_extract_preserves_file(tmp_path):
    """Test that extract doesn't modify the original file."""
    dummy_image = tmp_path / "preserve_test.png"
    original_content = "original content"
    dummy_image.write_text(original_content)

    ocr = MathOCR()
    ocr.extract(str(dummy_image))

    # File should still exist and have same content
    assert dummy_image.exists()
    assert dummy_image.read_text() == original_content


def test_extract_with_directory_path(tmp_path):
    """Test that extract handles directory path appropriately."""
    ocr = MathOCR()

    # Pass a directory instead of a file
    with pytest.raises((FileNotFoundError, IsADirectoryError, OSError)):
        ocr.extract(str(tmp_path))


def test_extract_with_none_path():
    """Test that extract handles None path appropriately."""
    ocr = MathOCR()

    with pytest.raises((TypeError, ValueError, AttributeError)):
        ocr.extract(None)


def test_extract_with_empty_string():
    """Test that extract handles empty string path."""
    ocr = MathOCR()

    with pytest.raises((FileNotFoundError, ValueError)):
        ocr.extract("")


def test_math_ocr_initialization():
    """Test MathOCR initialization."""
    ocr = MathOCR()

    assert ocr is not None
    assert hasattr(ocr, 'extract')
    assert hasattr(ocr, 'health_check')


def test_extract_returns_non_empty_string(tmp_path):
    """Test that extract always returns a non-empty string."""
    dummy_image = tmp_path / "test.png"
    dummy_image.write_text("content")

    ocr = MathOCR()
    math_text = ocr.extract(str(dummy_image))

    assert isinstance(math_text, str)
    assert len(math_text) > 0
    assert math_text.strip() != ""


def test_extract_different_instances(tmp_path):
    """Test that different MathOCR instances work independently."""
    dummy_image = tmp_path / "test.png"
    dummy_image.write_text("content")

    ocr1 = MathOCR()
    ocr2 = MathOCR()

    result1 = ocr1.extract(str(dummy_image))
    result2 = ocr2.extract(str(dummy_image))

    assert isinstance(result1, str)
    assert isinstance(result2, str)


def test_extract_result_format(tmp_path):
    """Test that extracted math text has expected format."""
    dummy_image = tmp_path / "format_test.png"
    dummy_image.write_text("content")

    ocr = MathOCR()
    math_text = ocr.extract(str(dummy_image))

    # Should be a string (could contain LaTeX, plain text, etc.)
    assert isinstance(math_text, str)
    # Should not be just whitespace
    assert len(math_text.strip()) > 0


def test_extract_with_math_symbols_in_filename(tmp_path):
    """Test extracting from file with math-like characters in filename."""
    filenames = [
        "equation_x+y=z.png",
        "formula_E=mc2.png",
        "integral.png"
    ]

    ocr = MathOCR()

    for filename in filenames:
        image_file = tmp_path / filename
        image_file.write_text("content")

        math_text = ocr.extract(str(image_file))
        assert isinstance(math_text, str)


@pytest.fixture
def math_ocr():
    """Fixture to provide a MathOCR instance."""
    return MathOCR()


def test_with_fixture(math_ocr, tmp_path):
    """Example test using pytest fixture."""
    dummy_image = tmp_path / "fixture_test.png"
    dummy_image.write_text("dummy content")

    math_text = math_ocr.extract(str(dummy_image))
    assert isinstance(math_text, str)


@pytest.mark.parametrize("extension", ["png", "jpg", "jpeg", "gif", "bmp", "tiff"])
def test_various_image_extensions(math_ocr, tmp_path, extension):
    """Test extracting from files with various image extensions."""
    image_file = tmp_path / f"math.{extension}"
    image_file.write_text("dummy content")

    math_text = math_ocr.extract(str(image_file))

    assert isinstance(math_text, str)
    assert len(math_text) > 0


@pytest.mark.parametrize("filename", [
    "equation.png",
    "math-formula.png",
    "integral_calc.png",
    "derivative (1).png",
    "summation[2].png",
    "complex123.png"
])
def test_various_filenames(math_ocr, tmp_path, filename):
    """Test extracting from files with various filename patterns."""
    image_file = tmp_path / filename
    image_file.write_text("dummy content")

    math_text = math_ocr.extract(str(image_file))

    assert isinstance(math_text, str)


def test_extract_with_unicode_filename(tmp_path):
    """Test extracting from file with Unicode characters in filename."""
    unicode_names = ["数学.png", "数式.png", "수식.png"]
    ocr = MathOCR()

    for name in unicode_names:
        try:
            image_file = tmp_path / name
            image_file.write_text("content")

            math_text = ocr.extract(str(image_file))
            assert isinstance(math_text, str)
        except (OSError, UnicodeError):
            # Some filesystems don't support Unicode filenames
            pytest.skip(f"Filesystem doesn't support Unicode filename: {name}")


def test_extract_consistent_behavior(tmp_path):
    """Test that extract behavior is consistent."""
    dummy_image = tmp_path / "consistent.png"
    dummy_image.write_text("content")

    ocr = MathOCR()

    # Call multiple times
    results = [ocr.extract(str(dummy_image)) for _ in range(3)]

    # All should be strings
    assert all(isinstance(r, str) for r in results)
    # All should be non-empty
    assert all(len(r) > 0 for r in results)


def test_extract_with_very_long_filename(tmp_path):
    """Test extracting from file with very long filename."""
    # Create a long but valid filename
    long_name = "math_" + "equation_" * 20 + ".png"

    try:
        image_file = tmp_path / long_name
        image_file.write_text("content")

        ocr = MathOCR()
        math_text = ocr.extract(str(image_file))

        assert isinstance(math_text, str)
    except OSError:
        # Filename too long for filesystem
        pytest.skip("Filename too long for filesystem")


def test_extract_placeholder_content(tmp_path):
    """Test that placeholder content is meaningful."""
    dummy_image = tmp_path / "placeholder_test.png"
    dummy_image.write_text("content")

    ocr = MathOCR()
    math_text = ocr.extract(str(dummy_image))

    # Placeholder should be informative
    assert isinstance(math_text, str)
    assert "placeholder" in math_text.lower()
    # Should indicate it's math-related
    assert len(math_text) > 5  # More than just "placeholder"