# code_analysis/tests/test_main_cli.py

import pytest
from fixtures.mock_analyzer import MockAnalyzer
import main

def test_cli_demo(monkeypatch, capsys):
    monkeypatch.setattr(main, "analyzer", MockAnalyzer())
    main.cli_demo()
    captured = capsys.readouterr()
    assert "Analysis result" in captured.out
    assert "Health check" in captured.out
