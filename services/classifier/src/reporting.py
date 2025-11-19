# classifier/src/reporting.py
"""
Responsible for reporting training metrics to Matrix
and printing to console.
"""

from libs.api_clients.matrix_wrapper import MatrixClientSync
from .metrics import MetricState


class Reporter:

    def __init__(self, config):
        self.client = MatrixClientSync(
            config.matrix.homeserver,
            config.matrix.user,
            config.matrix.password,
            config.matrix.room_id
        )

    def report(self, metrics: MetricState):
        """Send metrics to Matrix and print locally."""
        data = {
            "epoch": metrics.epoch,
            "loss": round(metrics.loss, 4),
            "accuracy": round(metrics.accuracy, 4)
        }
        print(f"[Epoch {metrics.epoch}] Reporting: {data}")
        self.client.send_ml_metrics(data)
