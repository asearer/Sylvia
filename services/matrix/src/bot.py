"""
Matrix Orchestration Bot Example
--------------------------------
Listens for custom events in Matrix and triggers workflow/ML jobs as needed.

- Edit bot credentials/room in environment or config.
- Extensible for deployments, status/command, more.
- docker-compose ready.
"""
import os
import asyncio
from libs.api-clients.matrix_wrapper import MatrixClientWrapper
from nio import RoomMessageText

MATRIX_HOMESERVER = os.environ.get("MATRIX_HOMESERVER", "https://matrix.org")
MATRIX_BOT_USER = os.environ.get("MATRIX_BOT_USER", "@botuser:matrix.org")
MATRIX_BOT_PASSWORD = os.environ.get("MATRIX_BOT_PASSWORD", "yourpassword")
MATRIX_ROOM_ID = os.environ.get("MATRIX_ROOM_ID", "!yourroomid:matrix.org")

def trigger_ml_job(payload=None):
    # Replace with actual ML pipeline trigger (or REST call, etc)
    print(f"[Bot] Triggered ML job with payload: {payload}")

class MatrixOrchestrationBot(MatrixClientWrapper):
    async def listen_and_respond(self):
        await self.login()
        print("[Bot] Listening for events to orchestrate...")
        self.client.add_event_callback(self._on_event, RoomMessageText)
        await self.client.join(self.room_id)
        while True:
            await self.client.sync(timeout=30000)
    async def _on_event(self, room, event):
        # Example: Respond to '!train' or custom events
        body = getattr(event, 'body', '')
        print(f"[Bot] Received event: {body}")
        if body.strip() == '!train':
            trigger_ml_job({'source': 'matrix', 'command': 'train'})
        # Extend here for other commands or events

if __name__ == '__main__':
    try:
        asyncio.run(MatrixOrchestrationBot(
            MATRIX_HOMESERVER, MATRIX_BOT_USER, MATRIX_BOT_PASSWORD, MATRIX_ROOM_ID
        ).listen_and_respond())
    except KeyboardInterrupt:
        print("[Bot] Shutting down.")
