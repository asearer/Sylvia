# classifier/tests/test_reporting.py

from classifier.src.reporting import Reporter
from classifier.src.metrics import MetricState
from fixtures.mock_matrix_client import MockMatrixClient
from fixtures.mock_config import get_mock_config


def test_reporting_sends_matrix(monkeypatch):
    cfg = get_mock_config()

    # Monkeypatch MatrixClientSync to our mock
    monkeypatch.setattr(
        "classifier.src.reporting.MatrixClientSync",
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
