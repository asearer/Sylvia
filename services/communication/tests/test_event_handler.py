# tests/test_event_handler.py

import pytest
import asyncio
from event_handler import EventHandler
from message_router import MessageRouter

# Mock async client
class MockClient:
    def __init__(self, name):
        self.name = name
        self.connected = True
        self.sent_messages = []
        self._callback = None

    async def connect(self):
        self.connected = True

    async def send_message(self, channel, message):
        self.sent_messages.append((channel, message))

    def register_message_callback(self, callback):
        self._callback = callback

    async def simulate_incoming_message(self, content="Hello"):
        if self._callback:
            self._callback({"content": content, "channel": "default"})

@pytest.mark.asyncio
async def test_event_handler_listen():
    # Setup mock clients
    discord = MockClient("discord")
    matrix = MockClient("matrix")
    clients = [discord, matrix]

    # Setup mock router that records routed messages
    class MockRouter:
        def __init__(self):
            self.routed = []

        def route_message(self, source, message):
            self.routed.append((source.name, message["content"]))

    router = MockRouter()
    handler = EventHandler(router)

    # Start listening in background
    listen_task = asyncio.create_task(handler.listen(clients))
    await asyncio.sleep(0.1)  # Let event handler register callbacks

    # Simulate messages
    await discord.simulate_incoming_message("Discord msg")
    await matrix.simulate_incoming_message("Matrix msg")

    await asyncio.sleep(0.1)  # Allow handler to route messages

    # Stop listening
    handler.stop()
    await asyncio.sleep(0.1)

    # Check that messages were routed
    routed_contents = [msg for _, msg in router.routed]
    assert "Discord msg" in routed_contents
    assert "Matrix msg" in routed_contents
