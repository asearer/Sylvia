import pytest
from discord_adapter import DiscordAdapter

def test_discord_adapter_instantiation():
    adapter = DiscordAdapter(token="dummy")
    assert adapter.token == "dummy"
