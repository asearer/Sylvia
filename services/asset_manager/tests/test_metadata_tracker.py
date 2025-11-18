from metadata_tracker import MetadataTracker

def test_track_get_metadata():
    mt = MetadataTracker()
    mt.track("item1", {"author": "Bob"})
    assert mt.get_metadata("item1")["author"] == "Bob"
