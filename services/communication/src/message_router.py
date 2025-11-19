"""
MessageRouter: Routes messages between multiple communication clients.
"""

import asyncio
import logging
from typing import List, Dict

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


class MessageRouter:
    def __init__(self, clients: List, default_channels: Dict = None):
        """
        Initialize the MessageRouter.

        Args:
            clients (List): List of communication client instances
            default_channels (Dict, optional): Maps client -> default channel/room
        """
        self.clients = clients
        self.default_channels = default_channels or {}

    async def route_message(self, source, message: dict):
        """
        Route a message from the source client to other clients.

        Args:
            source: The client that sent the message
            message (dict): Message dictionary with at least a 'content' key
        """
        tasks = []
        for client in self.clients:
            if client == source:
                continue  # Skip the source client
            try:
                channel = self.default_channels.get(client, "default_channel")
                if hasattr(client, "send_message"):
                    send = client.send_message
                    if asyncio.iscoroutinefunction(send):
                        tasks.append(send(channel, message["content"]))
                    else:
                        send(channel, message["content"])
                    logger.info(f"Routed message to {client}: {message['content']}")
            except Exception as e:
                logger.exception(f"Failed to route message to {client}: {e}")

        if tasks:
            await asyncio.gather(*tasks, return_exceptions=True)

    def add_client(self, client, default_channel: str = "default_channel"):
        """
        Add a new client to the router.

        Args:
            client: Communication client instance
            default_channel (str): Default channel/room for messages
        """
        self.clients.append(client)
        self.default_channels[client] = default_channel
        logger.info(f"Added client {client} with default channel {default_channel}")
