import pytest
from unittest.mock import AsyncMock, MagicMock, patch

@pytest.fixture
def dummy_creds():
    """Return dummy (homeserver, user, password, room_id) tuple."""
    return ('http://test-server', '@testuser', 'password', '!room:test')

@pytest.fixture
def async_matrix_client():
    with patch('libs.api-clients.matrix_wrapper.AsyncClient', autospec=True) as mock:
        mock.return_value.login = AsyncMock()
        mock.return_value.room_send = AsyncMock()
        yield mock

@pytest.fixture
def metric_event():
    """Factory for dummy metrics payload."""
    def _factory(epoch=1, accuracy=0.9, loss=0.1):
        return {'epoch': epoch, 'accuracy': accuracy, 'loss': loss}
    return _factory
