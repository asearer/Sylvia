import uuid
import logging
import json
import time
from typing import List, Dict, Optional
from threading import Lock, Thread, Event
from pathlib import Path
import asyncio

logger = logging.getLogger(__name__)

class CapsuleManager:
    """
    Manages capsules (grouped datasets for experiments) with:
    - Thread-safe access
    - Optional persistence to disk
    - Async-friendly interface
    - Automatic TTL-based cleanup
    - Optional background cleanup thread
    """

    def __init__(
        self,
        storage_file: Optional[str] = None,
        ttl_seconds: Optional[int] = None,
        background_cleanup: bool = False,
        cleanup_interval: float = 5.0  # seconds
    ):
        self._lock = Lock()
        self.storage_file = Path(storage_file) if storage_file else None
        self.ttl_seconds = ttl_seconds
        self.cleanup_interval = cleanup_interval

        # capsules stored as {capsule_id: {"datasets": [...], "created_at": timestamp}}
        self.capsules: Dict[str, Dict] = {}

        # Event to stop background cleanup thread
        self._stop_event = Event()
        self._cleanup_thread: Optional[Thread] = None

        # Load existing capsules from disk
        if self.storage_file and self.storage_file.exists():
            self._load_from_disk()

        # Start background cleanup if requested
        if background_cleanup and self.ttl_seconds is not None:
            self._start_background_cleanup()

    # -------------------------
    # Core methods
    # -------------------------
    def _cleanup_expired(self):
        """Remove expired capsules"""
        if self.ttl_seconds is None:
            return
        now = time.time()
        expired = [cid for cid, data in self.capsules.items()
                   if now - data["created_at"] > self.ttl_seconds]
        for cid in expired:
            del self.capsules[cid]
            logger.info(f"Expired capsule removed: {cid}")
        if expired:
            self._save_to_disk()

    def create(self, dataset_ids: List[str]) -> str:
        if not all(isinstance(d, str) for d in dataset_ids):
            raise ValueError("All dataset_ids must be strings")

        with self._lock:
            self._cleanup_expired()
            capsule_id = f"capsule_{uuid.uuid4().hex}"
            self.capsules[capsule_id] = {
                "datasets": dataset_ids,
                "created_at": time.time()
            }
            self._save_to_disk()
        logger.info(f"Created capsule {capsule_id} with datasets: {dataset_ids}")
        return capsule_id

    def get_capsule(self, capsule_id: str) -> List[str]:
        with self._lock:
            self._cleanup_expired()
            capsule = self.capsules.get(capsule_id)
        if capsule is None:
            logger.warning(f"Capsule {capsule_id} not found")
            return []
        return capsule["datasets"]

    def list_capsules(self) -> List[str]:
        with self._lock:
            self._cleanup_expired()
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
                self.capsules = {k: {"datasets": v["datasets"], "created_at": v["created_at"]}
                                 for k, v in data.items()}
            logger.debug(f"Loaded capsules from {self.storage_file}")
        except Exception as e:
            logger.error(f"Failed to load capsules: {e}")

    # -------------------------
    # Background cleanup
    # -------------------------
    def _start_background_cleanup(self):
        """Starts a background thread that periodically removes expired capsules"""
        if self._cleanup_thread is not None:
            return  # already running

        def cleanup_loop():
            while not self._stop_event.is_set():
                with self._lock:
                    self._cleanup_expired()
                self._stop_event.wait(self.cleanup_interval)

        self._cleanup_thread = Thread(target=cleanup_loop, daemon=True)
        self._cleanup_thread.start()
        logger.info("Started background TTL cleanup thread")

    def stop_background_cleanup(self):
        """Stops the background cleanup thread"""
        if self._cleanup_thread is None:
            return
        self._stop_event.set()
        self._cleanup_thread.join()
        self._cleanup_thread = None
        logger.info("Stopped background TTL cleanup thread")
