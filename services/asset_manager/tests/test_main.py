import os
import tempfile
import asyncio
import time
import pytest
from main import AssetManager
from pathlib import Path

# -----------------------
# Helpers
# -----------------------
def create_temp_file(content="test"):
    fd, path = tempfile.mkstemp()
    with os.fdopen(fd, "w") as f:
        f.write(content)
    return path

# -----------------------
# Basic Sync Test
# -----------------------
def test_asset_manager_sync():
    file_path = create_temp_file()
    am = AssetManager(
        dataset_storage_file=None,
        capsule_storage_file=None
    )

    dataset_id = am.ingest_dataset(file_path)
    assert dataset_id.startswith("dataset_")

    am.track_metadata(dataset_id, {"author": "Alice"})

    capsule_id = am.create_capsule([dataset_id])
    assert capsule_id.startswith("capsule_")

    os.remove(file_path)

# -----------------------
# Persistence Test
# -----------------------
def test_asset_manager_persistence():
    file_path = create_temp_file()
    with tempfile.TemporaryDirectory() as tmpdir:
        dataset_file = os.path.join(tmpdir, "datasets.json")
        capsule_file = os.path.join(tmpdir, "capsules.json")
        am1 = AssetManager(
            dataset_storage_file=dataset_file,
            capsule_storage_file=capsule_file
        )
        dataset_id = am1.ingest_dataset(file_path)
        capsule_id = am1.create_capsule([dataset_id])

        # Reload AssetManager
        am2 = AssetManager(
            dataset_storage_file=dataset_file,
            capsule_storage_file=capsule_file
        )
        # Dataset and capsule should still exist
        assert am2.create_capsule([dataset_id]).startswith("capsule_")
    os.remove(file_path)

# -----------------------
# Async Test
# -----------------------
@pytest.mark.asyncio
async def test_asset_manager_async():
    file_path = create_temp_file()
    am = AssetManager()
    dataset_id = await am.aingest_dataset(file_path)
    assert dataset_id.startswith("dataset_")

    await am.atrack_metadata(dataset_id, {"author": "Alice"})

    capsule_id = await am.acreate_capsule([dataset_id])
    assert capsule_id.startswith("capsule_")

    os.remove(file_path)

# -----------------------
# TTL / Cleanup Test
# -----------------------
def test_asset_manager_ttl_cleanup():
    file_path = create_temp_file()
    am = AssetManager(
        dataset_ttl=1,
        capsule_ttl=1,
        background_cleanup=False
    )
    dataset_id = am.ingest_dataset(file_path)
    capsule_id = am.create_capsule([dataset_id])

    # Wait for TTL expiration
    time.sleep(1.1)

    # Dataset and capsule should be expired
    dataset_path = am.dataset_manager.get_dataset(dataset_id)
    assert dataset_path is None

    capsule_data = am.capsule_manager.get_capsule(capsule_id)
    assert capsule_data == []

    os.remove(file_path)

# -----------------------
# Background Cleanup Thread Test
# -----------------------
def test_asset_manager_background_cleanup():
    file_path = create_temp_file()
    am = AssetManager(
        dataset_ttl=1,
        capsule_ttl=1,
        background_cleanup=True
    )
    dataset_id = am.ingest_dataset(file_path)
    capsule_id = am.create_capsule([dataset_id])

    # Wait longer than TTL for background thread
    time.sleep(1.5)

    assert am.dataset_manager.get_dataset(dataset_id) is None
    assert am.capsule_manager.get_capsule(capsule_id) == []

    am.dataset_manager.stop_background_cleanup()
    am.capsule_manager.stop_background_cleanup()
    os.remove(file_path)

# -----------------------
# Invalid Dataset Path
# -----------------------
def test_asset_manager_invalid_path():
    am = AssetManager()
    with pytest.raises(ValueError):
        am.ingest_dataset("/non/existent/path.csv")
