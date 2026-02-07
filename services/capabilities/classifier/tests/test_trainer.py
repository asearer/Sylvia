# classifier/tests/test_trainer.py

import sys
from pathlib import Path

# Add the src directory to the Python path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))
# Add the tests directory for fixtures
sys.path.insert(0, str(Path(__file__).parent))

from trainer import Trainer
from fixtures.mock_config import get_mock_config
from fixtures.mock_matrix_client import MockMatrixClient
from fixtures.mock_dataset import mock_dataset
import dataset as dataset_mod


def test_trainer_runs_full_loop(monkeypatch):
    cfg = get_mock_config()

    # Use mock dataset
    monkeypatch.setattr(dataset_mod, "load_synthetic_dataset", lambda: mock_dataset())

    # Replace MatrixClient
    monkeypatch.setattr(
        "reporting.MatrixClientSync",
        lambda homeserver, user, password, room: MockMatrixClient()
    )

    trainer = Trainer(cfg)
    trainer.train()

    # Trainer should report once per epoch
    assert len(trainer.reporter.client.sent_messages) == cfg.training.epochs