from math_ocr import MathOCR

def test_extract():
    ocr = MathOCR()
    text = ocr.extract("sample.png")
    assert "placeholder" in text
