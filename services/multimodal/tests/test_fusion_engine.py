from fusion_engine import FusionEngine

def test_fuse():
    fe = FusionEngine()
    fused = fe.fuse(["diag"], "math", [["a"]], "cap")
    assert isinstance(fused, dict)
