"""
Matrix Client Wrapper for ML microservices

Usage:
 1. Set your Matrix bot credentials (homeserver, user, password, room_id).
    -> These can be loaded from env variables, config file, or passed directly when creating the client.
 2. Use send_event or send_ml_metrics to send events (e.g., status, metrics).
 3. Use MatrixClientSync for simple blocking send in scripts.

Install requirements:
    pip install matrix-nio[http]
"""
import asyncio
from typing import Any, Dict

try:
    from nio import AsyncClient, LoginResponse, RoomSendResponse
except ImportError:
    raise ImportError("matrix-nio is required. Install with: pip install matrix-nio[http]")

class MatrixClientWrapper:
    def __init__(self, homeserver: str, user: str, password: str, room_id: str):
        self.homeserver = homeserver
        self.user = user
        self.password = password
        self.room_id = room_id
        self.client = AsyncClient(homeserver, user)
        self._logged_in = False

    async def login(self):
        if not self._logged_in:
            result = await self.client.login(self.password)
            if isinstance(result, LoginResponse):
                self._logged_in = True
            else:
                raise Exception(f"Failed to log in: {result}")

    async def send_event(self, event_type: str, content: Dict[str, Any]):
        if not self._logged_in:
            await self.login()
        resp = await self.client.room_send(
            room_id=self.room_id,
            message_type=event_type,
            content=content,
        )
        if not isinstance(resp, RoomSendResponse) or hasattr(resp, 'error'):
            raise Exception(f"Failed to send event: {resp}")

    async def send_ml_metrics(self, metrics: Dict[str, Any]):
        await self.send_event(
            event_type="ml.metrics",
            content={"msgtype": "m.text", "metrics": metrics},
        )

    async def close(self):
        await self.client.close()

class MatrixClientSync:
    """
    Synchronous wrapper for Matrix event sending (for scripts, quick use).
    """
    def __init__(self, homeserver: str, user: str, password: str, room_id: str):
        self.async_client = MatrixClientWrapper(homeserver, user, password, room_id)
        self.loop = asyncio.new_event_loop()

    def send_ml_metrics(self, metrics: Dict[str, Any]):
        self.loop.run_until_complete(self.async_client.send_ml_metrics(metrics))
        self.loop.run_until_complete(self.async_client.close())

    def send_event(self, event_type: str, content: Dict[str, Any]):
        self.loop.run_until_complete(self.async_client.send_event(event_type, content))
        self.loop.run_until_complete(self.async_client.close())

"""
# Configuration Example (Recommended: use environment variables or config files in production)
MATRIX_HOMESERVER = "https://matrix.org"   # e.g., "https://your-homeserver.tld"
MATRIX_BOT_USER = "@botuser:matrix.org"
MATRIX_BOT_PASSWORD = "yourpassword"
MATRIX_ROOM_ID = "!yourroomid:matrix.org"

# Example usage
if __name__ == "__main__":
    sender = MatrixClientSync(MATRIX_HOMESERVER, MATRIX_BOT_USER, MATRIX_BOT_PASSWORD, MATRIX_ROOM_ID)
    sender.send_ml_metrics({"epoch": 1, "accuracy": 0.91, "loss": 0.1})
"""
