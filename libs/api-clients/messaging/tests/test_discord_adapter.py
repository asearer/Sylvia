import pytest
import sys
from pathlib import Path

# Add the parent directory to the Python path
sys.path.insert(0, str(Path(__file__).parent.parent))

from discord_adapter import DiscordAdapter

def test_discord_adapter_instantiation():
    adapter = DiscordAdapter(token="dummy")
    assert adapter.token == "dummy"