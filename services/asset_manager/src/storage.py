import json
import pickle
import logging
from pathlib import Path
from threading import Lock
import asyncio

logger = logging.getLogger(__name__)

class Storage:
    """
    Handles low-level storage of datasets and capsules.
    Supports:
    - Filesystem storage
    - Thread-safe operations
    - Async interface
    - JSON or Pickle serialization
    """

    def __init__(self):
        self._lock = Lock()

    # -------------------------
    # Save / Load
    # -------------------------
    def save(self, item, path: str, format: str = "pickle"):
        """
        Save item to storage.

        Args:
            item: Dataset, capsule, or any serializable object
            path (str): Path to save
            format (str): "pickle" or "json"
        """
        path = Path(path)
        path.parent.mkdir(parents=True, exist_ok=True)

        with self._lock:
            try:
                if format == "json":
                    with path.open("w", encoding="utf-8") as f:
                        json.dump(item, f, indent=2)
                elif format == "pickle":
                    with path.open("wb") as f:
                        pickle.dump(item, f)
                else:
                    raise ValueError(f"Unsupported format: {format}")
                logger.info(f"Saved item to {path}")
            except Exception as e:
                logger.error(f"Failed to save item to {path}: {e}")
                raise

    def load(self, path: str, format: str = "pickle"):
        """
        Load item from storage.

        Args:
            path (str): Path to load
            format (str): "pickle" or "json"

        Returns:
            object: Loaded item
        """
        path = Path(path)
        if not path.exists():
            raise FileNotFoundError(f"No file found at {path}")

        with self._lock:
            try:
                if format == "json":
                    with path.open("r", encoding="utf-8") as f:
                        return json.load(f)
                elif format == "pickle":
                    with path.open("rb") as f:
                        return pickle.load(f)
                else:
                    raise ValueError(f"Unsupported format: {format}")
            except Exception as e:
                logger.error(f"Failed to load item from {path}: {e}")
                raise

    # -------------------------
    # Async interface
    # -------------------------
    async def asave(self, item, path: str, format: str = "pickle"):
        return await asyncio.to_thread(self.save, item, path, format)

    async def aload(self, path: str, format: str = "pickle"):
        return await asyncio.to_thread(self.load, path, format)
