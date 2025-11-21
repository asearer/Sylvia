import pytest
import sys
from pathlib import Path

# Add the parent directory to the Python path
sys.path.insert(0, str(Path(__file__).parent.parent))

from router import Router
from events import Event

def test_register_adapter():
    router = Router()
    class DummyAdapter:
        def receive_events(self):
            return [Event("dummy", "channel", "user", "msg", 0)]
    adapter = DummyAdapter()
    router.register_adapter(adapter)
    events = router.poll_events()
    assert len(events) == 1