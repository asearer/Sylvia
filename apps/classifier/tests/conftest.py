import pytest

@pytest.fixture
def dummy_metrics():
    def _factory(epoch=1, accuracy=0.91, loss=0.2):
        return {"epoch": epoch, "accuracy": accuracy, "loss": loss}
    return _factory
