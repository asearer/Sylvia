import uuid
import logging
import json
from typing import List, Dict, Optional
from threading import Lock
from pathlib import Path
import asyncio

logger = logging.getLogger(__name__)

class CapsuleManager:
    """
    Manages capsules (grouped datasets for experiments) with:
    - Thread-safe access
    - Optional persistence to disk
    - Async-friendly interface for non-blocking use
    """

    def __init__(self, storage_file: Optional[str] = None):
        self.capsules: Dict[str, List[str]] = {}
        self._lock = Lock()
        self.storage_file = Path(storage_file) if storage_file else None

        # Load existing capsules if file is provided
        if self.storage_file and self.storage_file.exists():
            self._load_from_disk()

    # -------------------------
    # Synchronous interface
    # -------------------------
    def create(self, dataset_ids: List[str]) -> str:
        if not all(isinstance(d, str) for d in dataset_ids):
            raise ValueError("All dataset_ids must be strings")

        capsule_id = f"capsule_{uuid.uuid4().hex}"
        with self._lock:
            self.capsules[capsule_id] = dataset_ids
            self._save_to_disk()
        logger.info(f"Created capsule {capsule_id} with datasets: {dataset_ids}")
        return capsule_id

    def get_capsule(self, capsule_id: str) -> List[str]:
        with self._lock:
            capsule = self.capsules.get(capsule_id)
        if capsule is None:
            logger.warning(f"Capsule {capsule_id} not found")
            return []
        return capsule

    def list_capsules(self) -> List[str]:
        with self._lock:
            return list(self.capsules.keys())

    def delete_capsule(self, capsule_id: str) -> bool:
        with self._lock:
            if capsule_id in self.capsules:
                del self.capsules[capsule_id]
                self._save_to_disk()
                logger.info(f"Deleted capsule {capsule_id}")
                return True
        logger.warning(f"Attempted to delete non-existent capsule {capsule_id}")
        return False

    # -------------------------
    # Async interface
    # -------------------------
    async def acreate(self, dataset_ids: List[str]) -> str:
        return await asyncio.to_thread(self.create, dataset_ids)

    async def aget_capsule(self, capsule_id: str) -> List[str]:
        return await asyncio.to_thread(self.get_capsule, capsule_id)

    async def alist_capsules(self) -> List[str]:
        return await asyncio.to_thread(self.list_capsules)

    async def adelete_capsule(self, capsule_id: str) -> bool:
        return await asyncio.to_thread(self.delete_capsule, capsule_id)

    # -------------------------
    # Persistence
    # -------------------------
    def _save_to_disk(self):
        if not self.storage_file:
            return
        try:
            with self.storage_file.open("w", encoding="utf-8") as f:
                json.dump(self.capsules, f, indent=2)
            logger.debug(f"Saved capsules to {self.storage_file}")
        except Exception as e:
            logger.error(f"Failed to save capsules: {e}")

    def _load_from_disk(self):
        try:
            with self.storage_file.open("r", encoding="utf-8") as f:
                data = json.load(f)
            if isinstance(data, dict):
                self.capsules = {k: list(v) for k, v in data.items()}
            logger.debug(f"Loaded capsules from {self.storage_file}")
        except Exception as e:
            logger.error(f"Failed to load capsules: {e}")
