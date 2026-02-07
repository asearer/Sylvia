"""
Entrypoint for the Data Service.

This module coordinates:
- DataService initialization
- Cache refresh operations
- Optional continuous service loop
"""

import asyncio
import argparse
import logging

from data_service import DataService

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("DataServiceMain")


async def run_service(refresh_once: bool = False, show: bool = False):
    """
    Core async runner for the data service.
    """
    service = DataService()

    if refresh_once:
        logger.info("Performing one-time data refresh...")
        await service.refresh()

    if show:
        data = await service.get_all()
        logger.info(f"Current data snapshot: {data}")

    # Example service loop (expand as needed)
    if not refresh_once and not show:
        logger.info("Starting Data Service loop... (Ctrl+C to exit)")
        try:
            while True:
                await service.refresh()
                await asyncio.sleep(10)  # refresh interval
        except asyncio.CancelledError:
            logger.info("Service loop cancelled.")
        except KeyboardInterrupt:
            logger.info("Shutting down gracefully...")


def main():
    parser = argparse.ArgumentParser(description="Run the Data Service")
    parser.add_argument("--refresh", action="store_true",
                        help="Perform a one-time refresh from external data source.")
    parser.add_argument("--show", action="store_true",
                        help="Display current data snapshot and exit.")

    args = parser.parse_args()

    asyncio.run(run_service(refresh_once=args.refresh, show=args.show))


if __name__ == "__main__":
    main()
