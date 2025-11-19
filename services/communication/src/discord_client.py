"""
DiscordClient: Handles Discord messaging and event integration.
Uses discord.py library (async) for bot connectivity.
"""

import asyncio
import logging
from typing import Optional, Callable
import discord

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


class DiscordClient:
    def __init__(self, token: str, default_channel: Optional[str] = None):
        """
        Initialize Discord client.

        Args:
            token (str): Discord bot token
            default_channel (str, optional): Default channel to send messages
        """
        self.token = token
        self.default_channel = default_channel
        self.connected = False
        self.client = discord.Client(intents=discord.Intents.default())
        self._event_callback: Optional[Callable[[dict], None]] = None

        # Register internal event
        @self.client.event
        async def on_ready():
            self.connected = True
            logger.info(f"Discord bot connected as {self.client.user}")

        @self.client.event
        async def on_message(message):
            if message.author == self.client.user:
                return  # Ignore self messages
            if self._event_callback:
                self._event_callback({
                    "channel": message.channel.name,
                    "content": message.content,
                    "author": str(message.author)
                })

    async def connect(self):
        """
        Connect to Discord API.
        """
        try:
            await self.client.start(self.token)
        except Exception as e:
            logger.exception(f"Failed to connect to Discord: {e}")
            self.connected = False

    async def send_message(self, channel_name: Optional[str], message: str):
        """
        Send message to a Discord channel.

        Args:
            channel_name (str): Channel name. Defaults to default_channel
            message (str): Message content
        """
        if not channel_name:
            channel_name = self.default_channel
        if not channel_name:
            raise ValueError("No channel specified for sending message")
        if not self.connected:
            logger.warning("Discord client not connected. Message not sent.")
            return

        for guild in self.client.guilds:
            channel = discord.utils.get(guild.text_channels, name=channel_name)
            if channel:
                await channel.send(message)
                logger.info(f"Sent message to {channel_name}")
                return
        logger.warning(f"Channel {channel_name} not found in any guilds")

    def register_message_callback(self, callback: Callable[[dict], None]):
        """
        Register a callback for incoming messages.

        Args:
            callback (Callable[[dict], None]): Function called with message dict
        """
        self._event_callback = callback

    async def disconnect(self):
        """
        Disconnect the Discord client.
        """
        await self.client.close()
        self.connected = False
        logger.info("Discord client disconnected")
