"""
Unit tests for TableExtractor module using pytest.
"""

import pytest
import os
from pathlib import Path
from table_extractor import TableExtractor


def test_extract_returns_list(tmp_path):
    """Test that extract returns a list with table data."""
    # Create a temporary dummy image file
    dummy_image = tmp_path / "dummy.png"
    dummy_image.write_text("dummy content")

    te = TableExtractor()
    tables = te.extract(str(dummy_image))

    assert isinstance(tables, list)
    assert len(tables) > 0
    assert tables == [["cell1", "cell2"], ["cell3", "cell4"]]


def test_extract_file_not_found():
    """Test that extract raises FileNotFoundError for non-existent file."""
    te = TableExtractor()

    with pytest.raises(FileNotFoundError):
        te.extract("nonexistent.png")


def test_health_check():
    """Test TableExtractor health check functionality."""
    te = TableExtractor()
    health = te.health_check()

    assert health["module"] == "TableExtractor"
    assert health["status"] == "initialized"
    assert isinstance(health, dict)


def test_extract_with_different_formats(tmp_path):
    """Test extracting from different image formats."""
    formats = ["png", "jpg", "jpeg", "gif", "bmp"]
    te = TableExtractor()

    for fmt in formats:
        image_file = tmp_path / f"table_image.{fmt}"
        image_file.write_text(f"dummy {fmt} content")

        tables = te.extract(str(image_file))
        assert isinstance(tables, list)


def test_extract_with_empty_file(tmp_path):
    """Test extracting from an empty image file."""
    empty_image = tmp_path / "empty.png"
    empty_image.write_text("")

    te = TableExtractor()
    tables = te.extract(str(empty_image))

    # Should return list (could be empty or with placeholder)
    assert isinstance(tables, list)


def test_extract_with_pathlib_path(tmp_path):
    """Test that extract accepts pathlib.Path objects."""
    dummy_image = tmp_path / "pathlib_test.png"
    dummy_image.write_text("dummy content")

    te = TableExtractor()
    tables = te.extract(dummy_image)  # Pass Path object directly

    assert isinstance(tables, list)


def test_extract_table_structure(tmp_path):
    """Test that extracted tables have correct structure."""
    dummy_image = tmp_path / "structure_test.png"
    dummy_image.write_text("dummy content")

    te = TableExtractor()
    tables = te.extract(str(dummy_image))

    assert isinstance(tables, list)
    # Each row should be a list
    for row in tables:
        assert isinstance(row, list)
        # Each cell should be a string
        for cell in row:
            assert isinstance(cell, str)


def test_extract_multiple_images(tmp_path):
    """Test extracting from multiple images sequentially."""
    te = TableExtractor()
    all_tables = []

    for i in range(5):
        image_file = tmp_path / f"table_{i}.png"
        image_file.write_text(f"content {i}")

        tables = te.extract(str(image_file))
        all_tables.append(tables)
        assert isinstance(tables, list)

    # All results should be lists
    assert all(isinstance(t, list) for t in all_tables)


def test_extract_same_image_multiple_times(tmp_path):
    """Test extracting from the same image multiple times."""
    dummy_image = tmp_path / "repeat_test.png"
    dummy_image.write_text("dummy content")

    te = TableExtractor()

    result1 = te.extract(str(dummy_image))
    result2 = te.extract(str(dummy_image))
    result3 = te.extract(str(dummy_image))

    # All should return valid lists
    assert isinstance(result1, list)
    assert isinstance(result2, list)
    assert isinstance(result3, list)


def test_extract_with_absolute_path(tmp_path):
    """Test extracting with absolute file path."""
    dummy_image = tmp_path / "absolute_test.png"
    dummy_image.write_text("dummy content")

    te = TableExtractor()
    absolute_path = str(dummy_image.absolute())
    tables = te.extract(absolute_path)

    assert isinstance(tables, list)


def test_extract_with_relative_path(tmp_path):
    """Test extracting with relative file path."""
    original_dir = os.getcwd()
    os.chdir(tmp_path)

    try:
        dummy_image = Path("relative_test.png")
        dummy_image.write_text("dummy content")

        te = TableExtractor()
        tables = te.extract("relative_test.png")

        assert isinstance(tables, list)
    finally:
        os.chdir(original_dir)


def test_extract_with_special_characters_in_filename(tmp_path):
    """Test extracting from file with special characters in name."""
    special_names = [
        "table-data.png",
        "table_data.png",
        "table data.png",
        "table(1).png",
        "table[2].png"
    ]

    te = TableExtractor()

    for name in special_names:
        image_file = tmp_path / name
        image_file.write_text("dummy content")

        tables = te.extract(str(image_file))
        assert isinstance(tables, list)


def test_extract_with_large_file(tmp_path):
    """Test extracting from a larger file."""
    large_image = tmp_path / "large.png"
    # Create a larger dummy file
    large_image.write_text("x" * 100000)

    te = TableExtractor()
    tables = te.extract(str(large_image))

    assert isinstance(tables, list)


def test_extract_preserves_file(tmp_path):
    """Test that extract doesn't modify the original file."""
    dummy_image = tmp_path / "preserve_test.png"
    original_content = "original content"
    dummy_image.write_text(original_content)

    te = TableExtractor()
    te.extract(str(dummy_image))

    # File should still exist and have same content
    assert dummy_image.exists()
    assert dummy_image.read_text() == original_content


def test_extract_with_directory_path(tmp_path):
    """Test that extract handles directory path appropriately."""
    te = TableExtractor()

    # Pass a directory instead of a file
    with pytest.raises((FileNotFoundError, IsADirectoryError, OSError)):
        te.extract(str(tmp_path))


def test_extract_with_none_path():
    """Test that extract handles None path appropriately."""
    te = TableExtractor()

    with pytest.raises((TypeError, ValueError, AttributeError)):
        te.extract(None)


def test_extract_with_empty_string():
    """Test that extract handles empty string path."""
    te = TableExtractor()

    with pytest.raises((FileNotFoundError, ValueError)):
        te.extract("")


def test_table_extractor_initialization():
    """Test TableExtractor initialization."""
    te = TableExtractor()

    assert te is not None
    assert hasattr(te, 'extract')
    assert hasattr(te, 'health_check')


def test_extract_returns_valid_table_format(tmp_path):
    """Test that extracted tables have valid format."""
    dummy_image = tmp_path / "format_test.png"
    dummy_image.write_text("content")

    te = TableExtractor()
    tables = te.extract(str(dummy_image))

    assert isinstance(tables, list)

    # If not empty, check structure
    if len(tables) > 0:
        # Should be list of lists (rows)
        assert all(isinstance(row, list) for row in tables)
        # All cells should be strings
        for row in tables:
            assert all(isinstance(cell, str) for cell in row)


def test_extract_table_dimensions(tmp_path):
    """Test that extracted table has expected dimensions."""
    dummy_image = tmp_path / "dimensions_test.png"
    dummy_image.write_text("content")

    te = TableExtractor()
    tables = te.extract(str(dummy_image))

    # Expected: 2 rows, 2 columns
    assert len(tables) == 2
    assert len(tables[0]) == 2
    assert len(tables[1]) == 2


def test_extract_cell_values(tmp_path):
    """Test that extracted cells have expected values."""
    dummy_image = tmp_path / "values_test.png"
    dummy_image.write_text("content")

    te = TableExtractor()
    tables = te.extract(str(dummy_image))

    # Check specific cell values
    assert tables[0][0] == "cell1"
    assert tables[0][1] == "cell2"
    assert tables[1][0] == "cell3"
    assert tables[1][1] == "cell4"


def test_extract_different_instances(tmp_path):
    """Test that different TableExtractor instances work independently."""
    dummy_image = tmp_path / "test.png"
    dummy_image.write_text("content")

    te1 = TableExtractor()
    te2 = TableExtractor()

    result1 = te1.extract(str(dummy_image))
    result2 = te2.extract(str(dummy_image))

    assert isinstance(result1, list)
    assert isinstance(result2, list)
    assert result1 == result2


def test_extract_empty_table(tmp_path):
    """Test handling of image with no tables."""
    # This depends on implementation - might return empty list
    dummy_image = tmp_path / "no_table.png"
    dummy_image.write_text("image with no tables")

    te = TableExtractor()
    tables = te.extract(str(dummy_image))

    assert isinstance(tables, list)


@pytest.fixture
def table_extractor():
    """Fixture to provide a TableExtractor instance."""
    return TableExtractor()


def test_with_fixture(table_extractor, tmp_path):
    """Example test using pytest fixture."""
    dummy_image = tmp_path / "fixture_test.png"
    dummy_image.write_text("dummy content")

    tables = table_extractor.extract(str(dummy_image))
    assert isinstance(tables, list)


@pytest.mark.parametrize("extension", ["png", "jpg", "jpeg", "gif", "bmp", "tiff"])
def test_various_image_extensions(table_extractor, tmp_path, extension):
    """Test extracting from files with various image extensions."""
    image_file = tmp_path / f"table.{extension}"
    image_file.write_text("dummy content")

    tables = table_extractor.extract(str(image_file))

    assert isinstance(tables, list)


@pytest.mark.parametrize("filename", [
    "simple_table.png",
    "table-with-dash.png",
    "table_with_underscore.png",
    "table with space.png",
    "table(1).png",
    "table123.png"
])
def test_various_filenames(table_extractor, tmp_path, filename):
    """Test extracting from files with various filename patterns."""
    image_file = tmp_path / filename
    image_file.write_text("dummy content")

    tables = table_extractor.extract(str(image_file))

    assert isinstance(tables, list)


def test_extract_with_unicode_filename(tmp_path):
    """Test extracting from file with Unicode characters in filename."""
    unicode_names = ["表格.png", "テーブル.png", "테이블.png"]
    te = TableExtractor()

    for name in unicode_names:
        try:
            image_file = tmp_path / name
            image_file.write_text("content")

            tables = te.extract(str(image_file))
            assert isinstance(tables, list)
        except (OSError, UnicodeError):
            # Some filesystems don't support Unicode filenames
            pytest.skip(f"Filesystem doesn't support Unicode filename: {name}")


def test_extract_consistent_behavior(tmp_path):
    """Test that extract behavior is consistent."""
    dummy_image = tmp_path / "consistent.png"
    dummy_image.write_text("content")

    te = TableExtractor()

    # Call multiple times
    results = [te.extract(str(dummy_image)) for _ in range(3)]

    # All should be lists
    assert all(isinstance(r, list) for r in results)
    # All should be equal
    assert all(r == results[0] for r in results)


def test_extract_table_not_empty(tmp_path):
    """Test that extracted table is not empty."""
    dummy_image = tmp_path / "not_empty.png"
    dummy_image.write_text("content")

    te = TableExtractor()
    tables = te.extract(str(dummy_image))

    # Should return at least the placeholder table
    assert len(tables) > 0
    assert len(tables[0]) > 0


def test_extract_all_cells_are_strings(tmp_path):
    """Test that all extracted cells are strings."""
    dummy_image = tmp_path / "strings_test.png"
    dummy_image.write_text("content")

    te = TableExtractor()
    tables = te.extract(str(dummy_image))

    for row in tables:
        for cell in row:
            assert isinstance(cell, str)
            # Cells should not be empty
            assert len(cell) > 0


def test_extract_rectangular_table(tmp_path):
    """Test that extracted table is rectangular (all rows same length)."""
    dummy_image = tmp_path / "rectangular.png"
    dummy_image.write_text("content")

    te = TableExtractor()
    tables = te.extract(str(dummy_image))

    if len(tables) > 0:
        # All rows should have same length
        row_lengths = [len(row) for row in tables]
        assert len(set(row_lengths)) == 1, "All rows should have same length"