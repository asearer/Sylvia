# code_analysis/tests/test_main_cli.py

import pytest
import sys
from pathlib import Path

# Add the parent directory to the Python path
sys.path.insert(0, str(Path(__file__).parent.parent))
# Add the tests directory for fixtures
sys.path.insert(0, str(Path(__file__).parent))

from fixtures.mock_analyzer import MockAnalyzer
import main

def test_cli_demo(monkeypatch, capsys):
    monkeypatch.setattr(main, "analyzer", MockAnalyzer())
    main.cli_demo()
    captured = capsys.readouterr()
    assert "Analysis result" in captured.out
    assert "Health check" in captured.out