from pipelines.autocomplete import AutocompleteEngine

def test_autocomplete_engine():
    engine = AutocompleteEngine()
    step = engine.suggest_next_step({})
    assert step == "next_step_placeholder"
