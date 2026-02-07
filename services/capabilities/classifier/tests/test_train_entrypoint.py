# classifier/tests/test_train_entrypoint.py

import sys
from pathlib import Path

# Add the src directory to the Python path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

import train as train_module

def test_train_entrypoint(monkeypatch):
    # Mock load_config
    monkeypatch.setattr(
        train_module,
        "load_config",
        lambda: "MOCK_CONFIG"
    )

    # Mock Trainer class
    class MockTrainer:
        def __init__(self, cfg):
            self.cfg = cfg
            self.called = False
        def train(self):
            self.called = True

    monkeypatch.setattr(train_module, "Trainer", MockTrainer)

    train_module.main()