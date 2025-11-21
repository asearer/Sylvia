import sys
from pathlib import Path

# Add the src directory to the Python path
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src"))

from context import Context

def test_context_set_get():
    ctx = Context()
    ctx.set("key", "value")
    assert ctx.get("key") == "value"