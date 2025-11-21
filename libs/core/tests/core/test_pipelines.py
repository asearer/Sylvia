import sys
from pathlib import Path

# Add the src directory to the Python path
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src"))

from pipelines.autocomplete import AutocompleteEngine

def test_autocomplete_engine():
    engine = AutocompleteEngine()
    step = engine.suggest_next_step({})
    assert step == "next_step_placeholder"