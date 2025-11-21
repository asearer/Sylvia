# code_analysis/tests/test_main_api.py

import pytest
from fastapi.testclient import TestClient
import sys
from pathlib import Path

# Add the parent directory to the Python path
sys.path.insert(0, str(Path(__file__).parent.parent))
# Add the tests directory for fixtures
sys.path.insert(0, str(Path(__file__).parent))

from main import app
from fixtures.mock_analyzer import MockAnalyzer
import main

@pytest.fixture(autouse=True)
def patch_analyzer(monkeypatch):
    monkeypatch.setattr(main, "analyzer", MockAnalyzer())

client = TestClient(app)

def test_health_endpoint():
    resp = client.get("/health")
    assert resp.status_code == 200
    data = resp.json()
    assert data["module"] == "CodeAnalyzer"

def test_analyze_endpoint_success():
    resp = client.post("/analyze", json={"code": "print('hello')"})
    assert resp.status_code == 200
    data = resp.json()
    assert "structure" in data
    assert "dependencies" in data
    assert "issues" in data

def test_analyze_endpoint_empty_code():
    resp = client.post("/analyze", json={"code": "   "})
    assert resp.status_code == 400
    assert "cannot be empty" in resp.json()["detail"]