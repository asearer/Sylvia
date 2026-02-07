
import asyncio
import websockets
import logging
import json
import sys
import threading

# Ensure libs approachability
sys.path.append("/app")

from libs.ipc.messenger import Messenger

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("avatar-bridge")

# Global variables
messenger = None
connected_clients = set()
loop = None

async def broadcast(message):
    """
    Broadcast a message to all connected WebSocket clients.
    """
    if not connected_clients:
        return
    
    # helper to ignore errors during send
    async def send_safe(client, msg):
        try:
            await client.send(msg)
        except:
            pass
            
    await asyncio.gather(
        *[send_safe(client, message) for client in connected_clients]
    )

async def handler(websocket):
    logger.info("Client connected")
    connected_clients.add(websocket)
    try:
        async for message in websocket:
            logger.info(f"Received: {message}")
            try:
                data = json.loads(message)
                # If valid JSON, publish to system (if it's a control message from Unity/Web)
                # For now we just log or forward "avatar_event"
                if messenger:
                    messenger.publish("avatar_event", data)
            except json.JSONDecodeError:
                pass
    except websockets.exceptions.ConnectionClosed:
        logger.info("Client disconnected")
    finally:
        connected_clients.remove(websocket)

async def start_server():
    # Disable CORS/Origin checks to allow connections from any host/browser
    async with websockets.serve(handler, "0.0.0.0", 8765, origins=None):
        logger.info("Avatar Bridge WebSocket Server started on port 8765 (CORS disabled)")
        await asyncio.Future()  # run forever

def redis_listener():
    """
    Listens to Redis events and forwards them to the asyncio loop for broadcasting.
    """
    global messenger, loop
    if not messenger:
        return
        
    def on_event(event_type, payload):
        try:
            # Re-serialize to JSON for the websocket client
            msg = json.dumps({"type": event_type, "payload": payload})
            if loop:
                asyncio.run_coroutine_threadsafe(broadcast(msg), loop)
        except Exception as e:
            logger.error(f"Broadcast error: {e}")

    logger.info("Redis Listener started")
    # This blocks, so run in thread
    messenger.subscribe(on_event)

async def main_async():
    global loop
    loop = asyncio.get_running_loop()
    
    # Start the Redis listener thread
    t = threading.Thread(target=redis_listener, daemon=True)
    t.start()
    
    await start_server()

def main():
    global messenger
    messenger = Messenger(channel="sylvia:events")
    
    try:
        asyncio.run(main_async())
    except KeyboardInterrupt:
        logger.info("Stopping Avatar Bridge...")

if __name__ == "__main__":
    main()
