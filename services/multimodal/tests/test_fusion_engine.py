"""
Unit tests for FusionEngine module using pytest.
"""

import pytest
from fusion_engine import FusionEngine


def test_fuse_returns_dict():
    """Test that fuse returns a dictionary with expected keys."""
    fe = FusionEngine()
    fused = fe.fuse(
        ["diag1", "diag2"],
        "E=mc^2",
        [["a", "b"], ["c", "d"]],
        "caption text"
    )

    assert isinstance(fused, dict)
    assert "diagrams" in fused
    assert "math" in fused
    assert "tables" in fused
    assert "captions" in fused


def test_fuse_content():
    """Test that fuse correctly stores all input content."""
    fe = FusionEngine()
    diagrams = ["diagram_placeholder"]
    math_text = "x+y=z"
    tables = [["1", "2"], ["3", "4"]]
    captions = "example caption"

    fused = fe.fuse(diagrams, math_text, tables, captions)

    assert fused["diagrams"] == diagrams
    assert fused["math"] == math_text
    assert fused["tables"] == tables
    assert fused["captions"] == captions


def test_health_check():
    """Test FusionEngine health check functionality."""
    fe = FusionEngine()
    health = fe.health_check()

    assert health["module"] == "FusionEngine"
    assert health["status"] == "initialized"
    assert isinstance(health, dict)


def test_fuse_with_empty_diagrams():
    """Test fuse with empty diagrams list."""
    fe = FusionEngine()
    fused = fe.fuse([], "math", [[]], "caption")

    assert isinstance(fused, dict)
    assert fused["diagrams"] == []


def test_fuse_with_empty_math():
    """Test fuse with empty math string."""
    fe = FusionEngine()
    fused = fe.fuse(["diag"], "", [[]], "caption")

    assert isinstance(fused, dict)
    assert fused["math"] == ""


def test_fuse_with_empty_tables():
    """Test fuse with empty tables list."""
    fe = FusionEngine()
    fused = fe.fuse(["diag"], "math", [], "caption")

    assert isinstance(fused, dict)
    assert fused["tables"] == []


def test_fuse_with_empty_captions():
    """Test fuse with empty captions string."""
    fe = FusionEngine()
    fused = fe.fuse(["diag"], "math", [[]], "")

    assert isinstance(fused, dict)
    assert fused["captions"] == ""


def test_fuse_with_all_empty():
    """Test fuse with all empty inputs."""
    fe = FusionEngine()
    fused = fe.fuse([], "", [], "")

    assert isinstance(fused, dict)
    assert fused["diagrams"] == []
    assert fused["math"] == ""
    assert fused["tables"] == []
    assert fused["captions"] == ""


def test_fuse_with_multiple_diagrams():
    """Test fuse with multiple diagram entries."""
    fe = FusionEngine()
    diagrams = ["diag1", "diag2", "diag3", "diag4", "diag5"]
    fused = fe.fuse(diagrams, "math", [[]], "caption")

    assert fused["diagrams"] == diagrams
    assert len(fused["diagrams"]) == 5


def test_fuse_with_complex_math():
    """Test fuse with complex mathematical expressions."""
    fe = FusionEngine()
    complex_math = "∫₀^∞ e^(-x²) dx = √π/2"
    fused = fe.fuse([], complex_math, [], "")

    assert fused["math"] == complex_math


def test_fuse_with_large_table():
    """Test fuse with a large table."""
    fe = FusionEngine()
    large_table = [[str(i), str(i + 1)] for i in range(100)]
    fused = fe.fuse([], "", large_table, "")

    assert fused["tables"] == large_table
    assert len(fused["tables"]) == 100


def test_fuse_with_nested_tables():
    """Test fuse with nested table structures."""
    fe = FusionEngine()
    tables = [
        [["a", "b"], ["c", "d"]],
        [["e", "f"], ["g", "h"]]
    ]
    fused = fe.fuse([], "", tables, "")

    assert fused["tables"] == tables


def test_fuse_with_long_caption():
    """Test fuse with a long caption text."""
    fe = FusionEngine()
    long_caption = "This is a very long caption " * 50
    fused = fe.fuse([], "", [], long_caption)

    assert fused["captions"] == long_caption


def test_fuse_with_special_characters():
    """Test fuse with special characters in all fields."""
    fe = FusionEngine()
    fused = fe.fuse(
        ["<diagram>", "diagram&text"],
        "α + β = γ",
        [["©", "®"], ["™", "€"]],
        "Caption with special chars: @#$%^&*()"
    )

    assert isinstance(fused, dict)
    assert "<diagram>" in fused["diagrams"]
    assert "α + β = γ" == fused["math"]


def test_fuse_preserves_data_types():
    """Test that fuse preserves input data types."""
    fe = FusionEngine()
    diagrams = ["d1", "d2"]
    math = "equation"
    tables = [[1, 2], [3, 4]]
    captions = "text"

    fused = fe.fuse(diagrams, math, tables, captions)

    assert isinstance(fused["diagrams"], list)
    assert isinstance(fused["math"], str)
    assert isinstance(fused["tables"], list)
    assert isinstance(fused["captions"], str)


def test_fuse_multiple_times():
    """Test calling fuse multiple times on same instance."""
    fe = FusionEngine()

    fused1 = fe.fuse(["d1"], "m1", [[]], "c1")
    fused2 = fe.fuse(["d2"], "m2", [[]], "c2")
    fused3 = fe.fuse(["d3"], "m3", [[]], "c3")

    # Each call should return independent results
    assert fused1["diagrams"] == ["d1"]
    assert fused2["diagrams"] == ["d2"]
    assert fused3["diagrams"] == ["d3"]


def test_fuse_does_not_modify_inputs():
    """Test that fuse doesn't modify input data."""
    fe = FusionEngine()

    diagrams = ["diag1", "diag2"]
    math = "E=mc^2"
    tables = [["a", "b"]]
    captions = "caption"

    # Store original values
    original_diagrams = diagrams.copy()
    original_tables = [row.copy() for row in tables]

    fused = fe.fuse(diagrams, math, tables, captions)

    # Inputs should remain unchanged
    assert diagrams == original_diagrams
    assert tables == original_tables


def test_fusion_engine_initialization():
    """Test FusionEngine initialization."""
    fe = FusionEngine()

    assert fe is not None
    assert hasattr(fe, 'fuse')
    assert hasattr(fe, 'health_check')


def test_fuse_with_none_values():
    """Test fuse behavior with None values."""
    fe = FusionEngine()

    # Depending on implementation, might raise TypeError or handle gracefully
    with pytest.raises((TypeError, ValueError, AttributeError)):
        fe.fuse(None, None, None, None)


def test_fuse_with_mixed_none():
    """Test fuse with some None values."""
    fe = FusionEngine()

    # Test various combinations - behavior depends on implementation
    try:
        fused = fe.fuse(["diag"], None, [], "caption")
        # If it succeeds, check the result
        assert isinstance(fused, dict)
    except (TypeError, AttributeError):
        # If it raises an error, that's also acceptable
        pass


@pytest.fixture
def fusion_engine():
    """Fixture to provide a FusionEngine instance."""
    return FusionEngine()


def test_with_fixture(fusion_engine):
    """Example test using pytest fixture."""
    fused = fusion_engine.fuse(["d"], "m", [[]], "c")
    assert isinstance(fused, dict)


@pytest.mark.parametrize("diagrams,math,tables,captions", [
    (["d1"], "m1", [[]], "c1"),
    (["d1", "d2"], "m2", [["a"]], "c2"),
    ([], "m3", [], "c3"),
    (["d"], "", [[]], ""),
])
def test_fuse_various_inputs(fusion_engine, diagrams, math, tables, captions):
    """Test fuse with various input combinations using parametrize."""
    fused = fusion_engine.fuse(diagrams, math, tables, captions)

    assert isinstance(fused, dict)
    assert fused["diagrams"] == diagrams
    assert fused["math"] == math
    assert fused["tables"] == tables
    assert fused["captions"] == captions


def test_fuse_result_has_all_keys():
    """Test that fused result always has all required keys."""
    fe = FusionEngine()
    fused = fe.fuse([], "", [], "")

    required_keys = ["diagrams", "math", "tables", "captions"]
    for key in required_keys:
        assert key in fused, f"Missing required key: {key}"


def test_fuse_with_unicode():
    """Test fuse with Unicode characters."""
    fe = FusionEngine()
    fused = fe.fuse(
        ["📊", "📈"],
        "∑ᵢ₌₁ⁿ xᵢ",
        [["中文", "日本語"], ["한국어", "العربية"]],
        "Caption avec émojis 🎉"
    )

    assert isinstance(fused, dict)
    assert "📊" in fused["diagrams"]