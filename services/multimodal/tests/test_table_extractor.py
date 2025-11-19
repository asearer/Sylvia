import pytest
from table_extractor import TableExtractor

def test_extract_returns_list(tmp_path):
    # Create a temporary dummy image file
    dummy_image = tmp_path / "dummy.png"
    dummy_image.write_text("dummy content")

    te = TableExtractor()
    tables = te.extract(str(dummy_image))
    assert isinstance(tables, list)
    assert tables == [["cell1", "cell2"], ["cell3", "cell4"]]

def test_extract_file_not_found():
    te = TableExtractor()
    with pytest.raises(FileNotFoundError):
        te.extract("nonexistent.png")

def test_health_check():
    te = TableExtractor()
    health = te.health_check()
    assert health["module"] == "TableExtractor"
    assert health["status"] == "initialized"
