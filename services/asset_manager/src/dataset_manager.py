import uuid
import logging
import json
import time
from typing import Dict, Optional
from threading import Lock, Thread, Event
from pathlib import Path
import asyncio

logger = logging.getLogger(__name__)

class DatasetManager:
    """
    Manages datasets: ingestion, storage, and retrieval, with:
    - Thread-safe access
    - Persistence to disk
    - Async-friendly interface
    - TTL-based automatic cleanup
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
        self.datasets: Dict[str, Dict] = {}  # {dataset_id: {"path": str, "created_at": float}}

        # Background cleanup control
        self._stop_event = Event()
        self._cleanup_thread: Optional[Thread] = None

        # Load existing datasets from disk
        if self.storage_file and self.storage_file.exists():
            self._load_from_disk()

        # Start background cleanup thread if requested
        if background_cleanup and ttl_seconds is not None:
            self._start_background_cleanup()

    # -------------------------
    # Core methods
    # -------------------------
    def _cleanup_expired(self):
        """Remove datasets older than TTL"""
        if self.ttl_seconds is None:
            return
        now = time.time()
        expired = [did for did, data in self.datasets.items()
                   if now - data["created_at"] > self.ttl_seconds]
        for did in expired:
            path = Path(self.datasets[did]["path"])
            if path.exists():
                try:
                    path.unlink()
                    logger.info(f"Deleted expired dataset file: {path}")
                except Exception as e:
                    logger.error(f"Failed to delete expired dataset file {path}: {e}")
            del self.datasets[did]
            logger.info(f"Expired dataset removed: {did}")
        if expired:
            self._save_to_disk()

    def ingest(self, dataset_path: str) -> str:
        path = Path(dataset_path)
        if not path.exists() or not path.is_file():
            raise ValueError(f"Dataset path does not exist or is not a file: {dataset_path}")

        dataset_id = f"dataset_{uuid.uuid4().hex}"
        with self._lock:
            self._cleanup_expired()
            self.datasets[dataset_id] = {
                "path": str(path.resolve()),
                "created_at": time.time()
            }
            self._save_to_disk()
        logger.info(f"Ingested dataset {dataset_id}: {dataset_path}")
        return dataset_id

    def get_dataset(self, dataset_id: str) -> Optional[str]:
        with self._lock:
            self._cleanup_expired()
            dataset = self.datasets.get(dataset_id)
        if dataset is None:
            logger.warning(f"Dataset {dataset_id} not found")
            return None
        return dataset["path"]

    def list_datasets(self) -> list[str]:
        with self._lock:
            self._cleanup_expired()
            return list(self.datasets.keys())

    def delete_dataset(self, dataset_id: str) -> bool:
        with self._lock:
            if dataset_id in self.datasets:
                path = Path(self.datasets[dataset_id]["path"])
                if path.exists():
                    try:
                        path.unlink()
                    except Exception as e:
                        logger.error(f"Failed to delete dataset file {path}: {e}")
                del self.datasets[dataset_id]
                self._save_to_disk()
                logger.info(f"Deleted dataset {dataset_id}")
                return True
        logger.warning(f"Attempted to delete non-existent dataset {dataset_id}")
        return False

    # -------------------------
    # Persistence
    # -------------------------
    def _save_to_disk(self):
        if not self.storage_file:
            return
        try:
            with self.storage_file.open("w", encoding="utf-8") as f:
                json.dump(self.datasets, f, indent=2)
            logger.debug(f"Saved datasets to {self.storage_file}")
        except Exception as e:
            logger.error(f"Failed to save datasets: {e}")

    def _load_from_disk(self):
        try:
            with self.storage_file.open("r", encoding="utf-8") as f:
                data = json.load(f)
            if isinstance(data, dict):
                self.datasets = {k: {"path": v["path"], "created_at": v["created_at"]} for k, v in data.items()}
            logger.debug(f"Loaded datasets from {self.storage_file}")
        except Exception as e:
            logger.error(f"Failed to load datasets: {e}")

    # -------------------------
    # Async interface
    # -------------------------
    async def aingest(self, dataset_path: str) -> str:
        return await asyncio.to_thread(self.ingest, dataset_path)

    async def aget_dataset(self, dataset_id: str) -> Optional[str]:
        return await asyncio.to_thread(self.get_dataset, dataset_id)

    async def alist_datasets(self) -> list[str]:
        return await asyncio.to_thread(self.list_datasets)

    async def adelete_dataset(self, dataset_id: str) -> bool:
        return await asyncio.to_thread(self.delete_dataset, dataset_id)

    # -------------------------
    # Background cleanup
    # -------------------------
    def _start_background_cleanup(self):
        """Starts a background thread that periodically removes expired datasets"""
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
