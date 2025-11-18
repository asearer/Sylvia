"""
Entrypoint for the Asset Manager service.
Coordinates datasets, metadata, and experiment capsules.
"""

from dataset_manager import DatasetManager
from metadata_tracker import MetadataTracker
from capsule_manager import CapsuleManager

class AssetManager:
    def __init__(self):
        self.dataset_manager = DatasetManager()
        self.metadata_tracker = MetadataTracker()
        self.capsule_manager = CapsuleManager()

    def ingest_dataset(self, dataset_path):
        return self.dataset_manager.ingest(dataset_path)

    def track_metadata(self, dataset_id, metadata):
        self.metadata_tracker.track(dataset_id, metadata)

    def create_capsule(self, dataset_ids):
        return self.capsule_manager.create(dataset_ids)

if __name__ == "__main__":
    am = AssetManager()
    am.ingest_dataset("data/sample.csv")
    am.track_metadata("dataset_1", {"author": "Alice"})
    capsule = am.create_capsule(["dataset_1"])
    print(capsule)
