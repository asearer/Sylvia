"""
Event normalization for messaging platforms.
"""

class Event:
    def __init__(self, platform: str, channel_id: str, user_id: str, content: str, timestamp: float):
        """
        Normalized event representation.

        Args:
            platform (str): Name of the messaging platform (e.g., 'matrix', 'discord').
            channel_id (str): Channel or room identifier.
            user_id (str): ID of the sender.
            content (str): Message content.
            timestamp (float): Unix timestamp of the event.
        """
        self.platform = platform
        self.channel_id = channel_id
        self.user_id = user_id
        self.content = content
        self.timestamp = timestamp
