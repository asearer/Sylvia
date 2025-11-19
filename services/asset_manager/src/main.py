import logging
from dataset_manager import DatasetManager
from metadata_tracker import MetadataTracker
from capsule_manager import CapsuleManager

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

class AssetManager:
    """
    Entrypoint for the Asset Manager service.
    Coordinates datasets, metadata, and experiment capsules.
    """

    def __init__(
        self,
        dataset_storage_file: str = None,
        capsule_storage_file: str = None,
        dataset_ttl: int = None,
        capsule_ttl: int = None,
        background_cleanup: bool = False
    ):
        self.dataset_manager = DatasetManager(
            storage_file=dataset_storage_file,
            ttl_seconds=dataset_ttl,
            background_cleanup=background_cleanup
        )
        self.metadata_tracker = MetadataTracker()
        self.capsule_manager = CapsuleManager(
            storage_file=capsule_storage_file,
            ttl_seconds=capsule_ttl,
            background_cleanup=background_cleanup
        )

    def ingest_dataset(self, dataset_path: str) -> str:
        try:
            dataset_id = self.dataset_manager.ingest(dataset_path)
            logger.info(f"Ingested dataset {dataset_id}")
            return dataset_id
        except Exception as e:
            logger.error(f"Failed to ingest dataset {dataset_path}: {e}")
            raise

    def track_metadata(self, dataset_id: str, metadata: dict):
        try:
            self.metadata_tracker.track(dataset_id, metadata)
            logger.info(f"Tracked metadata for dataset {dataset_id}")
        except Exception as e:
            logger.error(f"Failed to track metadata for dataset {dataset_id}: {e}")
            raise

    def create_capsule(self, dataset_ids: list[str]) -> str:
        try:
            capsule_id = self.capsule_manager.create(dataset_ids)
            logger.info(f"Created capsule {capsule_id} for datasets: {dataset_ids}")
            return capsule_id
        except Exception as e:
            logger.error(f"Failed to create capsule for datasets {dataset_ids}: {e}")
            raise

    # -------------------------
    # Async interface
    # -------------------------
    async def aingest_dataset(self, dataset_path: str) -> str:
        return await self.dataset_manager.aingest(dataset_path)

    async def atrack_metadata(self, dataset_id: str, metadata: dict):
        await asyncio.to_thread(self.track_metadata, dataset_id, metadata)

    async def acreate_capsule(self, dataset_ids: list[str]) -> str:
        return await self.capsule_manager.acreate(dataset_ids)


# -------------------------
# Example usage
# -------------------------
if __name__ == "__main__":
    am = AssetManager(
        dataset_storage_file="datasets.json",
        capsule_storage_file="capsules.json",
        dataset_ttl=3600,
        capsule_ttl=3600,
        background_cleanup=True
    )

    dataset_id = am.ingest_dataset("data/sample.csv")
    am.track_metadata(dataset_id, {"author": "Alice"})
    capsule_id = am.create_capsule([dataset_id])
    logger.info(f"Created capsule ID: {capsule_id}")
