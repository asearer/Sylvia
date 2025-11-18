from main import MultimodalReasoning

def test_process_image():
    mm = MultimodalReasoning()
    result = mm.process_image("sample.png")
    assert "diagrams" in result
    assert "math" in result
