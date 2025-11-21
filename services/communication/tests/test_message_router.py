# tests/test_message_router.py

import pytest
import asyncio
import sys
from pathlib import Path

# Add the parent directory to the Python path
sys.path.insert(0, str(Path(__file__).parent.parent))

from message_router import MessageRouter

# Mock async client
class MockClient:
    def __init__(self, name):
        self.name = name
        self.sent_messages = []

    async def send_message(self, channel, message):
        self.sent_messages.append((channel, message))

@pytest.mark.asyncio
async def test_route_message():
    # Setup mock clients
    discord = MockClient("discord")
    matrix = MockClient("matrix")
    clients = [discord, matrix]

    router = MessageRouter(clients, default_channels={discord: "discord_chan", matrix: "matrix_chan"})

    message = {"content": "Hello"}

    # Route message from discord
    await router.route_message(discord, message)

    # Discord should not receive its own message
    assert all(msg[1] != "Hello" for msg in discord.sent_messages)  # No messages to discord

    # Matrix should receive the message
    assert matrix.sent_messages[0][1] == "Hello"
    assert matrix.sent_messages[0][0] == "matrix_chan"