import pytest
from image_captioner import ImageCaptioner

def test_caption_returns_placeholder(tmp_path):
    # Create a temporary dummy image file
    dummy_image = tmp_path / "dummy.png"
    dummy_image.write_text("dummy content")

    ic = ImageCaptioner()
    caption = ic.caption(str(dummy_image))
    assert isinstance(caption, str)
    assert "placeholder" in caption

def test_caption_file_not_found():
    ic = ImageCaptioner()
    with pytest.raises(FileNotFoundError):
        ic.caption("nonexistent.png")

def test_health_check():
    ic = ImageCaptioner()
    health = ic.health_check()
    assert health["module"] == "ImageCaptioner"
    assert health["status"] == "initialized"
