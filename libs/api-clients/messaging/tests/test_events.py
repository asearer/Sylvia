import pytest
import sys
from pathlib import Path

# Add the parent directory to the Python path
sys.path.insert(0, str(Path(__file__).parent.parent))

from events import Event

def test_event_creation():
    e = Event("discord", "123", "u1", "Hello", 1234567890)
    assert e.platform == "discord"
    assert e.channel_id == "123"
    assert e.user_id == "u1"
    assert e.content == "Hello"