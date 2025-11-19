# classifier/tests/test_trainer.py

from classifier.src.trainer import Trainer
from fixtures.mock_config import get_mock_config
from fixtures.mock_matrix_client import MockMatrixClient
from fixtures.mock_dataset import mock_dataset
import classifier.src.dataset as dataset_mod


def test_trainer_runs_full_loop(monkeypatch):
    cfg = get_mock_config()

    # Use mock dataset
    monkeypatch.setattr(dataset_mod, "load_synthetic_dataset", lambda: mock_dataset())

    # Replace MatrixClient
    monkeypatch.setattr(
        "classifier.src.reporting.MatrixClientSync",
        lambda homeserver, user, password, room: MockMatrixClient()
    )

    trainer = Trainer(cfg)
    trainer.train()

    # Trainer should report once per epoch
    assert len(trainer.reporter.client.sent_messages) == cfg.training.epochs
