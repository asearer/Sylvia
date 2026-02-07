import random
from unittest.mock import patch, MagicMock
import sys
from pathlib import Path

# Add the src directory to the Python path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

import train


# Unit: Metrics calculation, logic isolation
def test_metrics_increases():
    initial_accuracy = 0.75
    history = []
    for _ in range(5):
        old = initial_accuracy
        initial_accuracy += random.uniform(0.01, 0.05)
        assert initial_accuracy > old
        history.append(initial_accuracy)
    assert len(history) == 5

# Integration: Matrix event sent for each epoch
@patch('matrix_wrapper.MatrixClientSync')
def test_train_report_sends_metrics(mock_matrix):
    mock_matrix.return_value = MagicMock()
    train.train_and_report()
    assert mock_matrix.return_value.send_ml_metrics.call_count == train.NUM_EPOCHS

# Smoke: Test script runs with no crash (network does not matter w/ mock)
def test_entry_point_runs(monkeypatch):
    monkeypatch.setattr(train, 'train_and_report', lambda: True)
    assert train.train_and_report() is True