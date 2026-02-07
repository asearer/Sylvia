# classifier/tests/test_metrics.py

import sys
from pathlib import Path

# Add the src directory to the Python path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from metrics import MetricState

def test_metric_state():
    m = MetricState(epoch=1, loss=0.5, accuracy=0.8)
    assert m.epoch == 1
    assert m.loss == 0.5
    assert m.accuracy == 0.8