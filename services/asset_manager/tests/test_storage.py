from storage import Storage

def test_storage_save_load():
    st = Storage()
    st.save("item", "path/to/file")
    loaded = st.load("path/to/file")
    assert "Loaded" in loaded
