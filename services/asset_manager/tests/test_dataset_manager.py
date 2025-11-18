from dataset_manager import DatasetManager

def test_ingest_get_dataset():
    dm = DatasetManager()
    dataset_id = dm.ingest("data/sample.csv")
    assert dm.get_dataset(dataset_id) == "data/sample.csv"
