# tests/test_communication_service.py

import pytest
import asyncio
import sys
from pathlib import Path

# Add the parent directory to the Python path
sys.path.insert(0, str(Path(__file__).parent.parent))

from main import CommunicationService

# Mock async clients
class MockAsyncClient:
    def __init__(self, name):
        self.name = name
        self.connected = False
        self.disconnected = False
        self.sent_messages = []

    async def connect(self):
        self.connected = True

    async def send_message(self, channel, message):
        self.sent_messages.append((channel, message))

    async def disconnect(self):
        self.disconnected = True

@pytest.mark.asyncio
async def test_communication_service_start(monkeypatch):
    # Setup mock clients
    mock_discord = MockAsyncClient("discord")
    mock_matrix = MockAsyncClient("matrix")

    # Patch the service to use mocks
    monkeypatch.setattr("main.DiscordClient", lambda *a, **kw: mock_discord)
    monkeypatch.setattr("main.MatrixClient", lambda *a, **kw: mock_matrix)

    service = CommunicationService(discord_token="fake", matrix_config={
        "homeserver": "https://matrix.org",
        "user_id": "@bot:matrix.org",
        "password": "fake",
        "default_room": "lobby"
    })

    # Start the service asynchronously in background
    start_task = asyncio.create_task(service.start_async())
    await asyncio.sleep(0.1)  # Let it run briefly
    service.event_handler.stop()  # Stop listening
    await asyncio.sleep(0.1)
    await service.shutdown()      # Shutdown clients

    # Check connections
    assert mock_discord.connected
    assert mock_matrix.connected
    assert mock_discord.disconnected
    assert mock_matrix.disconnected