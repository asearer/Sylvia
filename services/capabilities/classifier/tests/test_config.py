# classifier/tests/test_config.py

import os
import sys
from pathlib import Path

# Add the src directory to the Python path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from config import load_config

def test_load_config_env(monkeypatch):
    monkeypatch.setenv("MATRIX_HOMESERVER", "https://example.com")
    monkeypatch.setenv("MATRIX_USER", "@bot:test")
    monkeypatch.setenv("MATRIX_PASSWORD", "pass123")
    monkeypatch.setenv("MATRIX_ROOM_ID", "!room:test")

    cfg = load_config()

    assert cfg.matrix.homeserver == "https://example.com"
    assert cfg.matrix.user == "@bot:test"
    assert cfg.matrix.password == "pass123"
    assert cfg.matrix.room_id == "!room:test"