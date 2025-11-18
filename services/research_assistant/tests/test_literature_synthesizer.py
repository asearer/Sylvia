from literature_synthesizer import LiteratureSynthesizer

def test_synthesize():
    ls = LiteratureSynthesizer()
    summary = ls.synthesize(["doc1", "doc2"])
    assert isinstance(summary, str)
