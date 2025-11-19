"""
EventHandler: Listens to messages from multiple clients and triggers routing.
"""

import asyncio
import logging
from typing import List

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


class EventHandler:
    def __init__(self, router):
        """
        Initialize the EventHandler.

        Args:
            router: MessageRouter instance to route messages
        """
        self.router = router
        self._listening = False

    async def listen_client(self, client):
        """
        Listen for messages from a single client and route them.

        Args:
            client: Any client with `register_message_callback` or `receive_message`
        """
        try:
            # If client supports async callback registration
            if hasattr(client, "register_message_callback"):
                client.register_message_callback(lambda msg: self.router.route_message(client, msg))
            # If client only has synchronous receive_message (legacy)
            elif hasattr(client, "receive_message"):
                while self._listening:
                    msg = client.receive_message()
                    if msg:
                        self.router.route_message(client, msg)
                        logger.info(f"Routed message: {msg}")
                    await asyncio.sleep(1)
            else:
                logger.warning(f"Client {client} has no known message interface")
        except Exception as e:
            logger.exception(f"Error listening to client {client}: {e}")

    async def listen(self, clients: List):
        """
        Start listening to multiple clients concurrently.

        Args:
            clients (List): List of client instances
        """
        self._listening = True
        tasks = [self.listen_client(c) for c in clients]
        await asyncio.gather(*tasks)

    def stop(self):
        """
        Stop the event listener.
        """
        self._listening = False
        logger.info("EventHandler stopped listening")
