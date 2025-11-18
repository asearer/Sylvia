from main import AssetManager

def test_asset_manager():
    am = AssetManager()
    dataset_id = am.ingest_dataset("data/sample.csv")
    assert dataset_id.startswith("dataset_")
    am.track_metadata(dataset_id, {"author": "Alice"})
    capsule = am.create_capsule([dataset_id])
    assert capsule.startswith("capsule_")
