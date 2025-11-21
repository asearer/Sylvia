# classifier/tests/test_reporting.py

import sys
from pathlib import Path

# Add the src directory to the Python path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))
# Add the tests directory for fixtures
sys.path.insert(0, str(Path(__file__).parent))

from reporting import Reporter
from metrics import MetricState
from fixtures.mock_matrix_client import MockMatrixClient
from fixtures.mock_config import get_mock_config


def test_reporting_sends_matrix(monkeypatch):
    cfg = get_mock_config()

    # Monkeypatch MatrixClientSync to our mock
    monkeypatch.setattr(
        "reporting.MatrixClientSync",
        lambda homeserver, user, password, room: MockMatrixClient()
    )

    reporter = Reporter(cfg)
    metrics = MetricState(epoch=1, loss=0.33, accuracy=0.9)
    reporter.report(metrics)

    assert len(reporter.client.sent_messages) == 1
    sent = reporter.client.sent_messages[0]

    assert sent["epoch"] == 1
    assert sent["loss"] == 0.33
    assert sent["accuracy"] == 0.9