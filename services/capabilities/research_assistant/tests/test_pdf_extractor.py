from pdf_extractor import PDFExtractor

def test_extract_pdf():
    extractor = PDFExtractor()
    text = extractor.extract("dummy.pdf")
    assert "dummy.pdf" in text
