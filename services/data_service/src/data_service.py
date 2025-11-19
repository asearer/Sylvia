"""
DataService
-----------
Centralized shared data provider for Sylvia.

This module abstracts:
- Local cache access
- Remote API fetch (placeholder)
- File-based storage
- Async-safe data retrieval
- Pluggable data sources (Redis, DB, API)

The current implementation uses in-memory storage
with hooks for expanding into full infrastructure later.
"""

import asyncio
import logging
from typing import Any, Dict, List, Optional

logger = logging.getLogger(__name__)


class DataService:
    """
    Unified data retrieval + storage service.
    Designed to be dependency-free and mockable.
    """

    def __init__(self):
        self._cache: Dict[str, Any] = {}
        self._lock = asyncio.Lock()
        logger.info("DataService initialized")

    async def get(self, key: str) -> Optional[Any]:
        """
        Retrieve a value from the shared memory cache.
        Async-safe with locking.
        """
        async with self._lock:
            value = self._cache.get(key)
            logger.debug(f"DataService.get({key!r}) -> {value!r}")
            return value

    async def set(self, key: str, value: Any) -> None:
        """
        Store a value in the shared memory cache
        """
        async with self._lock:
            self._cache[key] = value
            logger.debug(f"DataService.set({key!r}, {value!r})")

    async def get_all(self) -> Dict[str, Any]:
        """
        Return a copy of all stored data.
        """
        async with self._lock:
            snapshot = dict(self._cache)
            logger.debug("DataService.get_all()")
            return snapshot

    async def fetch_external_data(self) -> List[Any]:
        """
        Async placeholder for external API/database fetch.

        Replace with:
        - API call
        - Database query
        - File loader
        - Library wrapper
        """
        logger.info("Fetching external data source...")
        await asyncio.sleep(0.1)  # simulate network latency
        return ["example", "data", "loaded"]

    async def refresh(self) -> None:
        """
        Refresh local cache from external source.
        """
        logger.info("Refreshing DataService cache...")
        data = await self.fetch_external_data()

        async with self._lock:
            self._cache["external"] = data
            logger.info("DataService cache refreshed")


# Convenience global instance (optional)
data_service = DataService()
