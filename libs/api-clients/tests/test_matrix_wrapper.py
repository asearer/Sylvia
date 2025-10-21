import pytest
from unittest.mock import patch, MagicMock, AsyncMock
from libs.api-clients import matrix_wrapper
import asyncio

@pytest.fixture
def creds():
    return ('http://local', '@user', 'pw', '!room:id')

@patch('libs.api-clients.matrix_wrapper.AsyncClient', autospec=True)
@pytest.mark.asyncio
async def test_login_success(mock_async, creds):
    cli = matrix_wrapper.MatrixClientWrapper(*creds)
    mock_async.return_value.login = AsyncMock(return_value=MagicMock())
    await cli.login()
    assert cli._logged_in

@patch('libs.api-clients.matrix_wrapper.AsyncClient', autospec=True)
@pytest.mark.asyncio
async def test_send_event_success(mock_async, creds):
    cli = matrix_wrapper.MatrixClientWrapper(*creds)
    cli._logged_in = True
    cli.client.room_send = AsyncMock(return_value=MagicMock())
    await cli.send_event('ml.metrics', {'metrics': {'acc': 1}})
    cli.client.room_send.assert_awaited()

@patch('libs.api-clients.matrix_wrapper.AsyncClient', autospec=True)
def test_sync_send_ml_metrics(mock_async, creds):
    cli_sync = matrix_wrapper.MatrixClientSync(*creds)
    cli_sync.async_client.send_ml_metrics = AsyncMock()
    cli_sync.async_client.close = AsyncMock()
    cli_sync.send_ml_metrics({'accuracy': 1})

@patch('libs.api-clients.matrix_wrapper.AsyncClient', autospec=True)
@pytest.mark.asyncio
async def test_send_event_failure_handling(mock_async, creds):
    cli = matrix_wrapper.MatrixClientWrapper(*creds)
    cli._logged_in = True
    cli.client.room_send = AsyncMock(return_value=MagicMock(error='fail'))
    with pytest.raises(Exception):
        await cli.send_event('ml.metrics', {'metrics': {'acc': 1}})
