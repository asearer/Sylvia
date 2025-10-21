import pytest
from unittest.mock import MagicMock

@pytest.fixture
def dummy_creds():
    return ('http://test-server', '@testuser', 'password', '!room:test')

@pytest.fixture
def dashboard_event():
    def _factory(type_='ml.metrics', content='{"epoch":1,"accuracy":0.9,"loss":0.1}'):
        event = MagicMock()
        event.body = content
        event.msgtype = type_
        return event
    return _factory
