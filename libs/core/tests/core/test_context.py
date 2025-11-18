from context import Context

def test_context_set_get():
    ctx = Context()
    ctx.set("key", "value")
    assert ctx.get("key") == "value"
