import json
from datetime import datetime
from typing import List, Dict, Optional, Union

class CustomMemory:
    """Enhanced memory storage for conversation history with personality evolution."""

    def __init__(self):
        """Initialize empty conversation history."""
        self.history: List[Dict] = []

    def add(self, message: str, speaker: str = "user", message_type: str = "text"):
        """
        Add a message to memory.

        Args:
            message (str): Message content
            speaker (str): 'user' or 'assistant'
            message_type (str): Type of message, e.g., 'text', 'command', 'event'
        """
        self.history.append({
            "timestamp": datetime.now(datetime.UTC).isoformat(),
            "speaker": speaker,
            "message": message,
            "type": message_type
        })

    def get(self, formatted: bool = True) -> Union[str, List[Dict]]:
        """
        Retrieve full conversation history.

        Args:
            formatted (bool): If True, returns as concatenated string; else raw list

        Returns:
            str | list: Conversation history
        """
        if formatted:
            return "\n".join(
                f"[{m['timestamp']}] {m['speaker']}: {m['message']}" for m in self.history
            )
        return self.history

    def clear(self):
        """Clear the conversation history."""
        self.history = []

    def snapshot(self, max_messages: int = 5) -> str:
        """
        Return a snapshot summary of the conversation for context or personality evolution.

        Args:
            max_messages (int): Number of user messages to include in the snapshot

        Returns:
            str: Concatenated snapshot messages
        """
        user_msgs = [m['message'] for m in self.history if m['speaker'] == 'user']
        return " ".join(user_msgs[:max_messages])

    def search(self, keyword: str, speaker: Optional[str] = None) -> List[Dict]:
        """
        Search for messages containing a keyword.

        Args:
            keyword (str): Term to search for
            speaker (str | None): Filter by speaker if provided

        Returns:
            list: Matching messages
        """
        results = [m for m in self.history if keyword.lower() in m['message'].lower()]
        if speaker:
            results = [m for m in results if m['speaker'] == speaker]
        return results

    def save(self, filepath: str):
        """
        Save conversation history to a JSON file.

        Args:
            filepath (str): File path to save the history
        """
        with open(filepath, "w") as f:
            json.dump(self.history, f, indent=2)

    def load(self, filepath: str):
        """
        Load conversation history from a JSON file.

        Args:
            filepath (str): File path to load the history from
        """
        with open(filepath, "r") as f:
            self.history = json.load(f)
