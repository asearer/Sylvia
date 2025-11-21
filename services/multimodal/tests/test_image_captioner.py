"""
Unit tests for ImageCaptioner module using pytest.
"""

import pytest
import os
from pathlib import Path
from image_captioner import ImageCaptioner


def test_caption_returns_placeholder(tmp_path):
    """Test that caption returns a string containing placeholder."""
    # Create a temporary dummy image file
    dummy_image = tmp_path / "dummy.png"
    dummy_image.write_text("dummy content")

    ic = ImageCaptioner()
    caption = ic.caption(str(dummy_image))

    assert isinstance(caption, str)
    assert len(caption) > 0
    assert "placeholder" in caption


def test_caption_file_not_found():
    """Test that caption raises FileNotFoundError for non-existent file."""
    ic = ImageCaptioner()

    with pytest.raises(FileNotFoundError):
        ic.caption("nonexistent.png")


def test_health_check():
    """Test ImageCaptioner health check functionality."""
    ic = ImageCaptioner()
    health = ic.health_check()

    assert health["module"] == "ImageCaptioner"
    assert health["status"] == "initialized"
    assert isinstance(health, dict)


def test_caption_with_different_formats(tmp_path):
    """Test captioning with different image formats."""
    formats = ["png", "jpg", "jpeg", "gif", "bmp"]
    ic = ImageCaptioner()

    for fmt in formats:
        image_file = tmp_path / f"test_image.{fmt}"
        image_file.write_text(f"dummy {fmt} content")

        caption = ic.caption(str(image_file))
        assert isinstance(caption, str)
        assert len(caption) > 0


def test_caption_with_empty_file(tmp_path):
    """Test captioning an empty image file."""
    empty_image = tmp_path / "empty.png"
    empty_image.write_text("")

    ic = ImageCaptioner()
    caption = ic.caption(str(empty_image))

    assert isinstance(caption, str)


def test_caption_with_pathlib_path(tmp_path):
    """Test that caption accepts pathlib.Path objects."""
    dummy_image = tmp_path / "pathlib_test.png"
    dummy_image.write_text("dummy content")

    ic = ImageCaptioner()
    caption = ic.caption(dummy_image)  # Pass Path object directly

    assert isinstance(caption, str)


def test_caption_multiple_images(tmp_path):
    """Test captioning multiple images sequentially."""
    ic = ImageCaptioner()
    captions = []

    for i in range(5):
        image_file = tmp_path / f"image_{i}.png"
        image_file.write_text(f"content {i}")

        caption = ic.caption(str(image_file))
        captions.append(caption)
        assert isinstance(caption, str)

    # All captions should be strings
    assert all(isinstance(c, str) for c in captions)


def test_caption_same_image_multiple_times(tmp_path):
    """Test captioning the same image multiple times."""
    dummy_image = tmp_path / "repeat_test.png"
    dummy_image.write_text("dummy content")

    ic = ImageCaptioner()

    caption1 = ic.caption(str(dummy_image))
    caption2 = ic.caption(str(dummy_image))
    caption3 = ic.caption(str(dummy_image))

    # All should return valid strings
    assert isinstance(caption1, str)
    assert isinstance(caption2, str)
    assert isinstance(caption3, str)


def test_caption_with_absolute_path(tmp_path):
    """Test captioning with absolute file path."""
    dummy_image = tmp_path / "absolute_test.png"
    dummy_image.write_text("dummy content")

    ic = ImageCaptioner()
    absolute_path = str(dummy_image.absolute())
    caption = ic.caption(absolute_path)

    assert isinstance(caption, str)


def test_caption_with_relative_path(tmp_path):
    """Test captioning with relative file path."""
    original_dir = os.getcwd()
    os.chdir(tmp_path)

    try:
        dummy_image = Path("relative_test.png")
        dummy_image.write_text("dummy content")

        ic = ImageCaptioner()
        caption = ic.caption("relative_test.png")

        assert isinstance(caption, str)
    finally:
        os.chdir(original_dir)


def test_caption_with_special_characters_in_filename(tmp_path):
    """Test captioning file with special characters in name."""
    special_names = [
        "test-image.png",
        "test_image.png",
        "test image.png",
        "test(1).png",
        "test[2].png"
    ]

    ic = ImageCaptioner()

    for name in special_names:
        image_file = tmp_path / name
        image_file.write_text("dummy content")

        caption = ic.caption(str(image_file))
        assert isinstance(caption, str)


def test_caption_with_large_file(tmp_path):
    """Test captioning a larger file."""
    large_image = tmp_path / "large.png"
    # Create a larger dummy file
    large_image.write_text("x" * 100000)

    ic = ImageCaptioner()
    caption = ic.caption(str(large_image))

    assert isinstance(caption, str)


def test_caption_preserves_file(tmp_path):
    """Test that caption doesn't modify the original file."""
    dummy_image = tmp_path / "preserve_test.png"
    original_content = "original content"
    dummy_image.write_text(original_content)

    ic = ImageCaptioner()
    ic.caption(str(dummy_image))

    # File should still exist and have same content
    assert dummy_image.exists()
    assert dummy_image.read_text() == original_content


def test_caption_with_directory_path(tmp_path):
    """Test that caption handles directory path appropriately."""
    ic = ImageCaptioner()

    # Pass a directory instead of a file
    with pytest.raises((FileNotFoundError, IsADirectoryError, OSError)):
        ic.caption(str(tmp_path))


def test_caption_with_none_path():
    """Test that caption handles None path appropriately."""
    ic = ImageCaptioner()

    with pytest.raises((TypeError, ValueError, AttributeError)):
        ic.caption(None)


def test_caption_with_empty_string():
    """Test that caption handles empty string path."""
    ic = ImageCaptioner()

    with pytest.raises((FileNotFoundError, ValueError)):
        ic.caption("")


def test_captioner_initialization():
    """Test ImageCaptioner initialization."""
    ic = ImageCaptioner()

    assert ic is not None
    assert hasattr(ic, 'caption')
    assert hasattr(ic, 'health_check')


def test_caption_returns_non_empty_string(tmp_path):
    """Test that caption always returns a non-empty string."""
    dummy_image = tmp_path / "test.png"
    dummy_image.write_text("content")

    ic = ImageCaptioner()
    caption = ic.caption(str(dummy_image))

    assert isinstance(caption, str)
    assert len(caption) > 0
    assert caption.strip() != ""


def test_caption_different_instances(tmp_path):
    """Test that different ImageCaptioner instances work independently."""
    dummy_image = tmp_path / "test.png"
    dummy_image.write_text("content")

    ic1 = ImageCaptioner()
    ic2 = ImageCaptioner()

    caption1 = ic1.caption(str(dummy_image))
    caption2 = ic2.caption(str(dummy_image))

    assert isinstance(caption1, str)
    assert isinstance(caption2, str)


@pytest.fixture
def captioner():
    """Fixture to provide an ImageCaptioner instance."""
    return ImageCaptioner()


def test_with_fixture(captioner, tmp_path):
    """Example test using pytest fixture."""
    dummy_image = tmp_path / "fixture_test.png"
    dummy_image.write_text("dummy content")

    caption = captioner.caption(str(dummy_image))
    assert isinstance(caption, str)


@pytest.mark.parametrize("extension", ["png", "jpg", "jpeg", "gif", "bmp", "tiff"])
def test_various_image_extensions(captioner, tmp_path, extension):
    """Test captioning files with various image extensions."""
    image_file = tmp_path / f"test.{extension}"
    image_file.write_text("dummy content")

    caption = captioner.caption(str(image_file))

    assert isinstance(caption, str)
    assert len(caption) > 0


@pytest.mark.parametrize("filename", [
    "simple.png",
    "with-dash.png",
    "with_underscore.png",
    "with space.png",
    "with(parens).png",
    "with123numbers.png"
])
def test_various_filenames(captioner, tmp_path, filename):
    """Test captioning files with various filename patterns."""
    image_file = tmp_path / filename
    image_file.write_text("dummy content")

    caption = captioner.caption(str(image_file))

    assert isinstance(caption, str)


def test_caption_with_unicode_filename(tmp_path):
    """Test captioning file with Unicode characters in filename."""
    unicode_names = ["图片.png", "画像.png", "이미지.png"]
    ic = ImageCaptioner()

    for name in unicode_names:
        try:
            image_file = tmp_path / name
            image_file.write_text("content")

            caption = ic.caption(str(image_file))
            assert isinstance(caption, str)
        except (OSError, UnicodeError):
            # Some filesystems don't support Unicode filenames
            pytest.skip(f"Filesystem doesn't support Unicode filename: {name}")


def test_caption_consistent_behavior(tmp_path):
    """Test that caption behavior is consistent."""
    dummy_image = tmp_path / "consistent.png"
    dummy_image.write_text("content")

    ic = ImageCaptioner()

    # Call multiple times
    results = [ic.caption(str(dummy_image)) for _ in range(3)]

    # All should be strings
    assert all(isinstance(r, str) for r in results)
    # All should be non-empty
    assert all(len(r) > 0 for r in results)