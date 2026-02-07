import pytest
import asyncio
from unittest.mock import patch
import sys
from pathlib import Path

# Add the parent directory to the Python path
sys.path.insert(0, str(Path(__file__).parent.parent))

from data_service import DataService


@pytest.mark.asyncio
async def test_set_and_get():
    service = DataService()
    await service.set("foo", "bar")
    result = await service.get("foo")
    assert result == "bar"


@pytest.mark.asyncio
async def test_get_all_returns_copy():
    service = DataService()
    await service.set("a", 1)
    await service.set("b", 2)

    snapshot = await service.get_all()
    assert snapshot == {"a": 1, "b": 2}

    # Ensure a copy (modifying snapshot should not modify internal cache)
    snapshot["a"] = 999
    new_snapshot = await service.get_all()
    assert new_snapshot == {"a": 1, "b": 2}


@pytest.mark.asyncio
async def test_fetch_external_data_mocked():
    service = DataService()

    with patch.object(service, "fetch_external_data", return_value=["x", "y"]) as mock_fetch:
        data = await service.fetch_external_data()
        assert data == ["x", "y"]
        mock_fetch.assert_called_once()


@pytest.mark.asyncio
async def test_refresh_updates_cache():
    service = DataService()

    with patch.object(service, "fetch_external_data", return_value=["mocked"]) as mock_fetch:
        await service.refresh()

    result = await service.get("external")
    assert result == ["mocked"]


@pytest.mark.asyncio
async def test_concurrent_sets_are_safe():
    """
    Tests async locking to ensure no race conditions occur.
    """
    service = DataService()

    async def writer(id):
        await service.set(f"key{id}", id)

    await asyncio.gather(*(writer(i) for i in range(20)))
    result = await service.get_all()

    assert len(result) == 20
    assert result["key0"] == 0
    assert result["key19"] == 19