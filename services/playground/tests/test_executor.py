"""
Tests for executor.py
"""

import pytest
import asyncio
from src.executor import CodeREPL, ExecutionResult


@pytest.mark.asyncio
async def test_code_repl_python_execution():
    """Test Python code execution."""
    repl = CodeREPL()
    result = await repl.execute("2 + 2", "python", 5)

    assert result["exit_code"] == 0
    assert result["output"] == "4"
    assert result["error"] is None


@pytest.mark.asyncio
async def test_code_repl_bash_execution():
    """Test Bash code execution."""
    repl = CodeREPL()
    result = await repl.execute("echo 'hello'", "bash", 5)

    assert result["exit_code"] == 0
    assert "hello" in result["output"]
    assert result["error"] is None


@pytest.mark.asyncio
async def test_code_repl_safety_filter():
    """Test safety filter blocks dangerous code."""
    repl = CodeREPL()
    result = await repl.execute("import os", "python", 5)

    assert result["exit_code"] == 1
    assert result["error"] == "Code rejected by safety filter"


@pytest.mark.asyncio
async def test_code_repl_timeout():
    """Test timeout enforcement."""
    repl = CodeREPL()
    result = await repl.execute("import time; time.sleep(10)", "bash", 1)

    assert result["exit_code"] == 124
    assert "timed out" in result["error"].lower()


@pytest.mark.asyncio
async def test_code_repl_invalid_language():
    """Test handling of invalid language."""
    repl = CodeREPL()
    result = await repl.execute("print('test')", "invalid_lang", 5)

    assert result["exit_code"] == 1
    assert "error" in result


def test_execution_result_to_dict():
    """Test ExecutionResult to_dict method."""
    result = ExecutionResult(output="test output", error=None, exit_code=0)
    result_dict = result.to_dict()

    assert result_dict["output"] == "test output"
    assert result_dict["error"] is None
    assert result_dict["exit_code"] == 0
