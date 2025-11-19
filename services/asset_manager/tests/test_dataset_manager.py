import os
import tempfile
import asyncio
import time
import pytest
from pathlib import Path
from dataset_manager import DatasetManager

# -----------------------
# Helpers
# -----------------------
def create_temp_file(content="test"):
    """Create a temporary file and return its path"""
    fd, path = tempfile.mkstemp()
    with os.fdopen(fd, "w") as f:
        f.write(content)
    return path

# -----------------------
# Sync Tests
# -----------------------
def test_ingest_and_get_dataset_sync():
    dm = DatasetManager()
    file_path = create_temp_file()
    dataset_id = dm.ingest(file_path)

    assert dm.get_dataset(dataset_id) == str(Path(file_path).resolve())
    assert dataset_id in dm.list_datasets()
    dm.delete_dataset(dataset_id)
    os.remove(file_path)

def test_delete_dataset_sync():
    dm = DatasetManager()
    file_path = create_temp_file()
    dataset_id = dm.ingest(file_path)

    assert dm.delete_dataset(dataset_id) is True
    assert dm.get_dataset(dataset_id) is None
    assert dm.delete_dataset("nonexistent") is False
    os.remove(file_path)

def test_invalid_path_sync():
    dm = DatasetManager()
    invalid_path = "/non/existent/path.csv"
    with pytest.raises(ValueError):
        dm.ingest(invalid_path)

# -----------------------
# Persistence Tests
# -----------------------
def test_persistence():
    file_path = create_temp_file()
    with tempfile.TemporaryDirectory() as tmpdir:
        storage_file = os.path.join(tmpdir, "datasets.json")
        dm = DatasetManager(storage_file=storage_file)
        dataset_id = dm.ingest(file_path)

        # Reload from disk
        dm2 = DatasetManager(storage_file=storage_file)
        assert dm2.get_dataset(dataset_id) == str(Path(file_path).resolve())
        assert dataset_id in dm2.list_datasets()
    os.remove(file_path)

# -----------------------
# TTL Tests
# -----------------------
def test_ttl_cleanup_sync():
    file_path = create_temp_file()
    dm = DatasetManager(ttl_seconds=1)
    dataset_id = dm.ingest(file_path)

    assert dm.get_dataset(dataset_id) == str(Path(file_path).resolve())
    time.sleep(1.1)  # wait for expiration
    assert dm.get_dataset(dataset_id) is None
    assert dataset_id not in dm.list_datasets()
    if os.path.exists(file_path):
        os.remove(file_path)

# -----------------------
# Background Cleanup Thread
# -----------------------
def test_background_cleanup():
    file_path = create_temp_file()
    dm = DatasetManager(ttl_seconds=1, background_cleanup=True, cleanup_interval=0.5)
    dataset_id = dm.ingest(file_path)
    time.sleep(1.5)  # wait for background cleanup
    assert dm.get_dataset(dataset_id) is None
    assert dataset_id not in dm.list_datasets()
    dm.stop_background_cleanup()
    if os.path.exists(file_path):
        os.remove(file_path)

# -----------------------
# Async Tests
# -----------------------
@pytest.mark.asyncio
async def test_async_ingest_and_get():
    file_path = create_temp_file()
    dm = DatasetManager()
    dataset_id = await dm.aingest(file_path)

    path = await dm.aget_dataset(dataset_id)
    assert path == str(Path(file_path).resolve())

    dataset_ids = await dm.alist_datasets()
    assert dataset_id in dataset_ids

    deleted = await dm.adelete_dataset(dataset_id)
    assert deleted is True
    os.remove(file_path)

@pytest.mark.asyncio
async def test_async_ttl_cleanup():
    file_path = create_temp_file()
    dm = DatasetManager(ttl_seconds=1)
    dataset_id = await dm.aingest(file_path)
    await asyncio.sleep(1.1)
    path = await dm.aget_dataset(dataset_id)
    assert path is None
    dataset_ids = await dm.alist_datasets()
    assert dataset_id not in dataset_ids
    if os.path.exists(file_path):
        os.remove(file_path)
