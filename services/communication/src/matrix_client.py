"""
MatrixClient: Handles Matrix messaging and event integration.
Uses matrix-nio async client.
"""

import asyncio
import logging
from typing import Optional, Callable
from nio import AsyncClient, RoomMessageText, LoginResponse

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


class MatrixClient:
    def __init__(self, homeserver: str, user_id: str, password: str, default_room: Optional[str] = None):
        """
        Initialize Matrix client.

        Args:
            homeserver (str): Matrix homeserver URL
            user_id (str): Matrix user ID (e.g., @bot:matrix.org)
            password (str): User password or access token
            default_room (str, optional): Default room to send messages
        """
        self.homeserver = homeserver
        self.user_id = user_id
        self.password = password
        self.default_room = default_room
        self.connected = False
        self.client = AsyncClient(homeserver, user_id)
        self._event_callback: Optional[Callable[[dict], None]] = None

    async def connect(self):
        """
        Connect and login to Matrix server.
        """
        try:
            response = await self.client.login(self.password)
            if isinstance(response, LoginResponse):
                self.connected = True
                logger.info(f"Matrix client logged in as {self.user_id}")
            else:
                self.connected = False
                logger.error(f"Matrix login failed: {response}")
        except Exception as e:
            logger.exception(f"Matrix connection error: {e}")
            self.connected = False

        # Add listener for incoming messages
        self.client.add_event_callback(self._on_message, RoomMessageText)

    async def _on_message(self, room, event):
        """
        Internal callback for incoming messages.

        Args:
            room: Room object
            event: Event object
        """
        if event.sender == self.user_id:
            return  # Ignore messages sent by self
        if self._event_callback:
            self._event_callback({
                "room": room.room_id,
                "content": event.body,
                "sender": event.sender
            })

    async def send_message(self, room: Optional[str], message: str):
        """
        Send message to a Matrix room.

        Args:
            room (str): Room ID or alias
            message (str): Message content
        """
        if not room:
            room = self.default_room
        if not room:
            raise ValueError("No room specified for sending message")
        if not self.connected:
            logger.warning("Matrix client not connected. Message not sent.")
            return

        try:
            await self.client.room_send(
                room_id=room,
                message_type="m.room.message",
                content={"msgtype": "m.text", "body": message}
            )
            logger.info(f"Sent message to {room}")
        except Exception as e:
            logger.exception(f"Failed to send message to {room}: {e}")

    def register_message_callback(self, callback: Callable[[dict], None]):
        """
        Register callback for incoming messages.

        Args:
            callback (Callable[[dict], None]): Function called with message dict
        """
        self._event_callback = callback

    async def disconnect(self):
        """
        Gracefully logout and close connection.
        """
        try:
            await self.client.logout()
            await self.client.close()
            self.connected = False
            logger.info("Matrix client disconnected")
        except Exception as e:
            logger.exception(f"Error during disconnect: {e}")
