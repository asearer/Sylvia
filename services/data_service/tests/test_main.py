import pytest
import asyncio
from unittest.mock import patch

from main import run_service


@pytest.mark.asyncio
async def test_run_service_refresh_once():
    with patch("data_service.DataService.refresh", return_value=None) as mock_refresh:
        await run_service(refresh_once=True)

    mock_refresh.assert_called_once()


@pytest.mark.asyncio
async def test_run_service_show():
    with patch("data_service.DataService.get_all", return_value={"x": 1}) as mock_get:
        await run_service(show=True)

    mock_get.assert_called_once()


@pytest.mark.asyncio
async def test_run_service_loop_starts_and_stops():
    """
    Ensure the infinite loop can be cancelled gracefully.
    """

    async def canceller(task):
        await asyncio.sleep(0.1)
        task.cancel()

    with patch("data_service.DataService.refresh", return_value=None):
        task = asyncio.create_task(run_service(refresh_once=False, show=False))
        asyncio.create_task(canceller(task))

        try:
            await task
        except asyncio.CancelledError:
            pass  # expected
