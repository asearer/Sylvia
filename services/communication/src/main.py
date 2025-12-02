"""
Communication Service Entrypoint.

This module serves as the central hub for external communication integrations.
It manages connections to platforms like Discord and Matrix, routing messages
between them and the internal event bus.

It supports an "Offline/Mock" mode for development without credentials.
"""

import asyncio
import logging
import argparse
from discord_client import DiscordClient
from matrix_client import MatrixClient
from message_router import MessageRouter
from event_handler import EventHandler

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


class CommunicationService:
    def __init__(self, discord_token: str, matrix_config: dict):
        """
        Initialize the Communication Service with clients and router.

        Args:
            discord_token (str): Discord bot token
            matrix_config (dict): Matrix credentials (homeserver, user_id, password, default_room)
        """
        self.discord = DiscordClient(token=discord_token, default_channel="general")
        self.matrix = MatrixClient(
            homeserver=matrix_config.get("homeserver"),
            user_id=matrix_config.get("user_id"),
            password=matrix_config.get("password"),
            default_room=matrix_config.get("default_room", "lobby")
        )

        self.router = MessageRouter([self.discord, self.matrix])
        self.event_handler = EventHandler(self.router)
        self.loop = asyncio.get_event_loop()

    async def start_async(self):
        """
        Start async clients and event handler.
        """
        logger.info("Starting CommunicationService...")
        await asyncio.gather(
            self.discord.connect(),
            self.matrix.connect()
        )
        # Start listening for events
        await self.event_handler.listen([self.discord, self.matrix])

    def start(self):
        """
        Run the service in the asyncio loop.
        """
        try:
            self.loop.run_until_complete(self.start_async())
        except KeyboardInterrupt:
            logger.info("CommunicationService interrupted, shutting down...")
        finally:
            self.loop.run_until_complete(self.shutdown())

    async def shutdown(self):
        """
        Gracefully shutdown clients.
        """
        await asyncio.gather(
            self.discord.disconnect(),
            self.matrix.disconnect()
        )
        self.loop.stop()
        logger.info("CommunicationService shutdown complete.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run Communication Service")
    parser.add_argument("--discord-token", type=str, required=False, help="Discord bot token")
    parser.add_argument("--matrix-homeserver", type=str, required=False)
    parser.add_argument("--matrix-user", type=str, required=False)
    parser.add_argument("--matrix-password", type=str, required=False)
    parser.add_argument("--matrix-room", type=str, default="lobby")
    args = parser.parse_args()

    # Check for credentials
    if not args.discord_token or not args.matrix_homeserver:
        logger.warning("Missing credentials. Starting in OFFLINE/MOCK mode.")
        # In offline mode, we just keep the process alive but don't connect
        try:
            while True:
                import time
                time.sleep(3600)
        except KeyboardInterrupt:
            logger.info("Offline mode interrupted.")
    else:
        matrix_cfg = {
            "homeserver": args.matrix_homeserver,
            "user_id": args.matrix_user,
            "password": args.matrix_password,
            "default_room": args.matrix_room
        }

        service = CommunicationService(discord_token=args.discord_token, matrix_config=matrix_cfg)
        service.start()
