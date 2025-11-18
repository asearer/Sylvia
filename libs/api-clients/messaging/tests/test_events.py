import pytest
from events import Event

def test_event_creation():
    e = Event("discord", "123", "u1", "Hello", 1234567890)
    assert e.platform == "discord"
    assert e.channel_id == "123"
    assert e.user_id == "u1"
    assert e.content == "Hello"
