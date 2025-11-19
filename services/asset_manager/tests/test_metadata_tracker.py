import os
import tempfile
import asyncio
import pytest
from pathlib import Path
from metadata_tracker import MetadataTracker

# -----------------------
# Helpers
# -----------------------
def create_temp_storage():
    tmpdir = tempfile.TemporaryDirectory()
    return os.path.join(tmpdir.name, "metadata.json"), tmpdir

# -----------------------
# Sync Tests
# -----------------------
def test_metadata_tracker_sync():
    mt = MetadataTracker()
    mt.track("item_1", {"author": "Alice"})
    assert mt.get_metadata("item_1") == {"author": "Alice"}
    assert "item_1" in mt.list_items()

    # Test deletion
    assert mt.delete_metadata("item_1") is True
    assert mt.get_metadata("item_1") == {}
    assert mt.delete_metadata("nonexistent") is False

def test_metadata_invalid_input_sync():
    mt = MetadataTracker()
    with pytest.raises(ValueError):
        mt.track("item_1", ["not", "a", "dict"])

# -----------------------
# Persistence Tests
# -----------------------
def test_metadata_persistence():
    storage_file, tmpdir = create_temp_storage()
    mt1 = MetadataTracker(storage_file=storage_file)
    mt1.track("item_1", {"author": "Alice"})
    mt1.track("item_2", {"author": "Bob"})

    # Reload metadata tracker
    mt2 = MetadataTracker(storage_file=storage_file)
    assert mt2.get_metadata("item_1") == {"author": "Alice"}
    assert mt2.get_metadata("item_2") == {"author": "Bob"}
    tmpdir.cleanup()

# -----------------------
# Async Tests
# -----------------------
@pytest.mark.asyncio
async def test_metadata_async():
    mt = MetadataTracker()
    await mt.atrack("item_1", {"author": "Alice"})
    metadata = await mt.aget_metadata("item_1")
    assert metadata == {"author": "Alice"}

    items = await mt.alist_items()
    assert "item_1" in items

    deleted = await mt.adelete_metadata("item_1")
    assert deleted is True
    metadata_after = await mt.aget_metadata("item_1")
    assert metadata_after == {}
