import pytest
from fusion_engine import FusionEngine

def test_fuse_returns_dict():
    fe = FusionEngine()
    fused = fe.fuse(["diag1", "diag2"], "E=mc^2", [["a","b"],["c","d"]], "caption text")
    assert isinstance(fused, dict)
    assert "diagrams" in fused
    assert "math" in fused
    assert "tables" in fused
    assert "captions" in fused

def test_fuse_content():
    fe = FusionEngine()
    diagrams = ["diagram_placeholder"]
    math_text = "x+y=z"
    tables = [["1","2"],["3","4"]]
    captions = "example caption"
    fused = fe.fuse(diagrams, math_text, tables, captions)
    assert fused["diagrams"] == diagrams
    assert fused["math"] == math_text
    assert fused["tables"] == tables
    assert fused["captions"] == captions

def test_health_check():
    fe = FusionEngine()
    health = fe.health_check()
    assert health["module"] == "FusionEngine"
    assert health["status"] == "initialized"
