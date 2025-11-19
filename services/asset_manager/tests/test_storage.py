import os
import tempfile
import asyncio
import pytest
from storage import Storage
from pathlib import Path

# -----------------------
# Helpers
# -----------------------
def create_temp_path(filename="test.pkl"):
    tmpdir = tempfile.TemporaryDirectory()
    return os.path.join(tmpdir.name, filename), tmpdir

# -----------------------
# Sync Tests
# -----------------------
def test_storage_save_load_pickle():
    st = Storage()
    path, tmpdir = create_temp_path("item.pkl")
    data = {"key": "value"}

    # Save
    st.save(data, path, format="pickle")
    assert Path(path).exists()

    # Load
    loaded = st.load(path, format="pickle")
    assert loaded == data

    tmpdir.cleanup()

def test_storage_save_load_json():
    st = Storage()
    path, tmpdir = create_temp_path("item.json")
    data = {"key": "value"}

    # Save
    st.save(data, path, format="json")
    assert Path(path).exists()

    # Load
    loaded = st.load(path, format="json")
    assert loaded == data

    tmpdir.cleanup()

def test_storage_invalid_format():
    st = Storage()
    path, tmpdir = create_temp_path("item.abc")
    data = {"key": "value"}

    with pytest.raises(ValueError):
        st.save(data, path, format="unsupported")

    tmpdir.cleanup()

def test_storage_load_nonexistent():
    st = Storage()
    path, tmpdir = create_temp_path("nonexistent.pkl")

    with pytest.raises(FileNotFoundError):
        st.load(path, format="pickle")

    tmpdir.cleanup()

# -----------------------
# Async Tests
# -----------------------
@pytest.mark.asyncio
async def test_storage_async_pickle():
    st = Storage()
    path, tmpdir = create_temp_path("async.pkl")
    data = {"key": "value"}

    await st.asave(data, path, format="pickle")
    loaded = await st.aload(path, format="pickle")
    assert loaded == data

    tmpdir.cleanup()

@pytest.mark.asyncio
async def test_storage_async_json():
    st = Storage()
    path, tmpdir = create_temp_path("async.json")
    data = {"key": "value"}

    await st.asave(data, path, format="json")
    loaded = await st.aload(path, format="json")
    assert loaded == data

    tmpdir.cleanup()
