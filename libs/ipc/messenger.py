
import json
import logging
import os
import redis
from typing import Callable, Any

logger = logging.getLogger(__name__)

class Messenger:
    """
    Simple Redis-based Messenger for IPC.
    """
    def __init__(self, redis_host: str = "redis", redis_port: int = 6379, channel: str = "sylvia:events"):
        self.redis_host = os.getenv("REDIS_HOST", redis_host)
        self.redis_port = int(os.getenv("REDIS_PORT", redis_port))
        self.channel = channel
        self.pub = redis.Redis(host=self.redis_host, port=self.redis_port, decode_responses=True)
        self.sub = redis.Redis(host=self.redis_host, port=self.redis_port, decode_responses=True)
        self.pubsub = self.sub.pubsub()

    def publish(self, event_type: str, payload: Any):
        """
        Publish an event to the channel.
        """
        message = json.dumps({"type": event_type, "payload": payload})
        try:
            self.pub.publish(self.channel, message)
            logger.debug(f"Published: {message}")
        except Exception as e:
            logger.error(f"Failed to publish message: {e}")

    def subscribe(self, handler: Callable[[str, Any], None]):
        """
        Subscribe to the channel and process messages with the handler.
        This runs in a blocking loop (or should be run in a thread).
        """
        self.pubsub.subscribe(self.channel)
        logger.info(f"Subscribed to {self.channel}")
        
        for message in self.pubsub.listen():
            if message["type"] == "message":
                try:
                    data = json.loads(message["data"])
                    event_type = data.get("type")
                    payload = data.get("payload")
                    if event_type and payload is not None:
                        handler(event_type, payload)
                except json.JSONDecodeError:
                    logger.error("Failed to decode JSON message")
                except Exception as e:
                    logger.error(f"Error processing message: {e}")

    def close(self):
        self.pub.close()
        self.sub.close()
