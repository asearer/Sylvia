"""
Custom memory module for LangChain conversation tracking.
Tracks conversation history and allows personality evolution.
"""

class CustomMemory:
    """Memory storage for conversation history."""

    def __init__(self):
        """Initialize empty conversation history."""
        self.history = []

    def add(self, message: str):
        """
        Add a message to memory.

        Args:
            message (str): Message to store
        """
        self.history.append(message)

    def get(self) -> str:
        """
        Retrieve full conversation history.

        Returns:
            str: Concatenated conversation messages
        """
        return "\n".join(self.history)

    def clear(self):
        """Clear the conversation history."""
        self.history = []
