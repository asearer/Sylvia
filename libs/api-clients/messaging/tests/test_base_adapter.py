import pytest
import sys
from pathlib import Path

# Add the parent directory to the Python path
sys.path.insert(0, str(Path(__file__).parent.parent))

from base_adapter import BaseAdapter

def test_base_adapter_instantiation():
    class DummyAdapter(BaseAdapter):
        def connect(self): pass
        def send_message(self, channel_id, message): pass
        def receive_events(self): return []

    adapter = DummyAdapter(token="dummy")
    assert adapter.token == "dummy"