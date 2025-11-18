"""
Abstract base class for messaging adapters.
Defines the interface for sending, receiving, and processing events.
"""

from abc import ABC, abstractmethod

class BaseAdapter(ABC):
    def __init__(self, token: str):
        """
        Initialize adapter with authentication token or credentials.

        Args:
            token (str): API token or key for the platform.
        """
        self.token = token

    @abstractmethod
    def connect(self):
        """Connect to the messaging platform."""
        raise NotImplementedError

    @abstractmethod
    def send_message(self, channel_id: str, message: str):
        """
        Send a message to a specific channel.

        Args:
            channel_id (str): Target channel or room.
            message (str): Message content.
        """
        raise NotImplementedError

    @abstractmethod
    def receive_events(self):
        """
        Listen or fetch events/messages from the platform.
        Returns:
            list: A list of normalized Event objects.
        """
        raise NotImplementedError
