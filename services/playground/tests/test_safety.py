"""
Tests for safety.py
"""

import pytest
from src.safety import Safety


def test_safety_is_safe_with_safe_code():
    """Test that safe code passes."""
    safety = Safety()
    assert safety.is_safe("x = 1 + 1")
    assert safety.is_safe("print('hello')")
    assert safety.is_safe("for i in range(10): print(i)")


def test_safety_blocks_dangerous_imports():
    """Test that dangerous imports are blocked."""
    safety = Safety()
    assert not safety.is_safe("import os")
    assert not safety.is_safe("import sys")
    assert not safety.is_safe("import subprocess")
    assert not safety.is_safe("from os import path")


def test_safety_blocks_dangerous_operations():
    """Test that dangerous operations are blocked."""
    safety = Safety()
    assert not safety.is_safe("open('file.txt', 'w')")
    assert not safety.is_safe("eval('1+1')")
    assert not safety.is_safe("exec('print(1)')")


def test_safety_blocks_network_operations():
    """Test that network operations are blocked."""
    safety = Safety()
    assert not safety.is_safe("import socket")
    assert not safety.is_safe("import requests")
    assert not safety.is_safe("curl http://example.com")


def test_safety_filter_code_raises_on_unsafe():
    """Test that filter_code raises ValueError on unsafe code."""
    safety = Safety()
    with pytest.raises(ValueError, match="dangerous patterns"):
        safety.filter_code("import os")


def test_safety_filter_code_returns_safe_code():
    """Test that filter_code returns safe code unchanged."""
    safety = Safety()
    code = "x = 1 + 1"
    assert safety.filter_code(code) == code


def test_safety_get_violations():
    """Test that get_violations returns list of violations."""
    safety = Safety()
    violations = safety.get_violations("import os; eval('1+1')")
    assert len(violations) > 0
    assert any("import" in v.lower() for v in violations)
