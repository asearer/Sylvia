# tests/test_matrix_client.py

import pytest
import asyncio
import sys
from pathlib import Path

# Add the parent directory to the Python path
sys.path.insert(0, str(Path(__file__).parent.parent))

from matrix_client import MatrixClient

# Mock AsyncClient to avoid network calls
class MockAsyncClient:
    def __init__(self, *args, **kwargs):
        self.logged_in = False
        self.room_send_calls = []

    async def login(self, password):
        self.logged_in = True
        return "LoginResponse"

    async def room_send(self, room_id, message_type, content):
        self.room_send_calls.append((room_id, content))
        return True

    def add_event_callback(self, callback, event_type):
        self._callback = callback

    async def logout(self):
        self.logged_in = False

    async def close(self):
        pass

@pytest.mark.asyncio
async def test_matrix_client_connect(monkeypatch):
    client = MatrixClient("https://matrix.org", "@bot:matrix.org", "fake", default_room="lobby")
    monkeypatch.setattr(client, "client", MockAsyncClient())
    await client.connect()
    assert client.connected

@pytest.mark.asyncio
async def test_matrix_client_send_message(monkeypatch):
    client = MatrixClient("https://matrix.org", "@bot:matrix.org", "fake", default_room="lobby")
    mock_client = MockAsyncClient()
    monkeypatch.setattr(client, "client", mock_client)
    client.connected = True
    await client.send_message("lobby", "Hello Matrix")
    assert mock_client.room_send_calls[0][0] == "lobby"
    assert mock_client.room_send_calls[0][1]["body"] == "Hello Matrix"

@pytest.mark.asyncio
async def test_matrix_client_register_message_callback(monkeypatch):
    client = MatrixClient("https://matrix.org", "@bot:matrix.org", "fake", default_room="lobby")
    callback_called = []

    def my_callback(msg):
        callback_called.append(msg)

    client.register_message_callback(my_callback)
    # Simulate incoming message
    if client._event_callback:
        client._event_callback({"room": "lobby", "content": "Test"})
    assert callback_called[0]["content"] == "Test"