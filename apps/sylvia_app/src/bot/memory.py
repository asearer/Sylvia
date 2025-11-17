# src/bot/memory.py

"""
MemoryBank for SylviaBot.

Stores user inputs per profile for evolving default responses.
"""

class MemoryBank:
    def __init__(self):
        self.storage = {}  # {profile_name: [messages]}

    def add(self, message: str, profile: str = "default") -> None:
        """Add a message to the memory for a given profile."""
        self.storage.setdefault(profile, []).append(message)

    def recall(self, profile: str = "default") -> str:
        """Return all remembered messages for a given profile."""
        return " ".join(self.storage.get(profile, []))
