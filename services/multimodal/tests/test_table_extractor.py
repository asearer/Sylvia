from table_extractor import TableExtractor

def test_extract():
    te = TableExtractor()
    tables = te.extract("sample.png")
    assert isinstance(tables, list)
