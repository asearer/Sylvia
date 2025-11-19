# code_analysis/tests/test_analyzer.py

import pytest
from analyzer import CodeAnalyzer

@pytest.fixture
def simple_code():
    return """
import os
import sys

def foo():
    for i in range(5):
        print(i)
"""

def test_analyze_structure(simple_code):
    analyzer = CodeAnalyzer()
    result = analyzer.analyze_code(simple_code)
    assert "structure" in result
    assert "dependencies" in result
    assert "issues" in result
    assert any(item["type"] == "function" for item in result["structure"])

def test_detect_imports(simple_code):
    analyzer = CodeAnalyzer()
    result = analyzer.analyze_code(simple_code)
    assert "os" in result["dependencies"]
    assert "sys" in result["dependencies"]

def test_nested_loop_detection():
    code = "for i in range(5):\n for j in range(3):\n  print(i, j)"
    analyzer = CodeAnalyzer()
    result = analyzer.analyze_code(code)
    assert any("Nested loop" in issue for issue in result["issues"])

def test_magic_number_detection():
    code = "x = 42\ny = 100"
    analyzer = CodeAnalyzer()
    result = analyzer.analyze_code(code)
    assert any("Magic numbers" in issue for issue in result["issues"])

def test_health_check():
    analyzer = CodeAnalyzer()
    health = analyzer.health_check()
    assert health["module"] == "CodeAnalyzer"
    assert "status" in health
