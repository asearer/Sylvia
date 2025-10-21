import pytest
from unittest.mock import MagicMock, patch

@pytest.fixture
def dummy_creds():
    return ('http://local', '@bot', 'pw', '!room:test')

@pytest.fixture
def bot_event():
    def _factory(body='!train'):
        event = MagicMock()
        event.body = body
        return event
    return _factory

@pytest.fixture(autouse=True)
def patch_trigger_ml_job():
    with patch('services.matrix.src.bot.trigger_ml_job') as patcher:
        yield patcher
