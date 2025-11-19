import json
import logging
from threading import Lock
from typing import Dict, Optional
from pathlib import Path
import asyncio

logger = logging.getLogger(__name__)

class MetadataTracker:
    """
    Tracks metadata for datasets and capsules with:
    - Thread-safe access
    - Optional persistence to disk
    - Async-friendly interface
    """

    def __init__(self, storage_file: Optional[str] = None):
        self._lock = Lock()
        self.storage_file = Path(storage_file) if storage_file else None
        self.metadata: Dict[str, dict] = {}

        if self.storage_file and self.storage_file.exists():
            self._load_from_disk()

    # -------------------------
    # Core methods
    # -------------------------
    def track(self, item_id: str, metadata: dict):
        """
        Track metadata for a dataset or capsule.
        """
        if not isinstance(metadata, dict):
            raise ValueError("metadata must be a dictionary")

        with self._lock:
            self.metadata[item_id] = metadata
            self._save_to_disk()
        logger.info(f"Tracked metadata for {item_id}")

    def get_metadata(self, item_id: str) -> dict:
        with self._lock:
            return self.metadata.get(item_id, {})

    def list_items(self) -> list[str]:
        with self._lock:
            return list(self.metadata.keys())

    def delete_metadata(self, item_id: str) -> bool:
        with self._lock:
            if item_id in self.metadata:
                del self.metadata[item_id]
                self._save_to_disk()
                logger.info(f"Deleted metadata for {item_id}")
                return True
        logger.warning(f"Attempted to delete non-existent metadata for {item_id}")
        return False

    # -------------------------
    # Persistence
    # -------------------------
    def _save_to_disk(self):
        if not self.storage_file:
            return
        try:
            with self.storage_file.open("w", encoding="utf-8") as f:
                json.dump(self.metadata, f, indent=2)
            logger.debug(f"Saved metadata to {self.storage_file}")
        except Exception as e:
            logger.error(f"Failed to save metadata: {e}")

    def _load_from_disk(self):
        try:
            with self.storage_file.open("r", encoding="utf-8") as f:
                data = json.load(f)
            if isinstance(data, dict):
                self.metadata = {k: dict(v) for k, v in data.items()}
            logger.debug(f"Loaded metadata from {self.storage_file}")
        except Exception as e:
            logger.error(f"Failed to load metadata: {e}")

    # -------------------------
    # Async interface
    # -------------------------
    async def atrack(self, item_id: str, metadata: dict):
        return await asyncio.to_thread(self.track, item_id, metadata)

    async def aget_metadata(self, item_id: str) -> dict:
        return await asyncio.to_thread(self.get_metadata, item_id)

    async def alist_items(self) -> list[str]:
        return await asyncio.to_thread(self.list_items)

    async def adelete_metadata(self, item_id: str) -> bool:
        return await asyncio.to_thread(self.delete_metadata, item_id)
