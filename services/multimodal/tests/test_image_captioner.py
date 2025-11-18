from image_captioner import ImageCaptioner

def test_caption():
    ic = ImageCaptioner()
    caption = ic.caption("sample.png")
    assert "placeholder" in caption
