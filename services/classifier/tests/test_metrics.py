# classifier/tests/test_metrics.py

from classifier.src.metrics import MetricState

def test_metric_state():
    m = MetricState(epoch=1, loss=0.5, accuracy=0.8)
    assert m.epoch == 1
    assert m.loss == 0.5
    assert m.accuracy == 0.8
