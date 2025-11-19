# tests/test_discord_client.py

import pytest
import asyncio
from discord_client import DiscordClient

# Async pytest fixture for DiscordClient
@pytest.fixture
def mock_discord_client():
    # Use dummy token for testing
    return DiscordClient(token="fake-token", default_channel="general")

@pytest.mark.asyncio
async def test_discord_connect(mock_discord_client, monkeypatch):
    # Patch the internal client start to simulate connection
    async def fake_start(token):
        mock_discord_client.connected = True
    monkeypatch.setattr(mock_discord_client.client, "start", fake_start)

    await mock_discord_client.connect()
    assert mock_discord_client.connected is True

@pytest.mark.asyncio
async def test_send_message(mock_discord_client, monkeypatch):
    # Patch send to just record call
    sent_messages = []

    async def fake_send(channel, msg):
        sent_messages.append((channel, msg))

    monkeypatch.setattr(mock_discord_client.client, "guilds", [])
    monkeypatch.setattr(mock_discord_client, "send_message", fake_send)

    await mock_discord_client.send_message("general", "Hello Test")
    assert sent_messages == [("general", "Hello Test")]

@pytest.mark.asyncio
async def test_register_message_callback(mock_discord_client):
    received = []

    def callback(msg):
        received.append(msg)

    mock_discord_client.register_message_callback(callback)
    # Simulate incoming message
    mock_discord_client._event_callback({"channel": "general", "content": "Hi"})
    assert received[0]["content"] == "Hi"
