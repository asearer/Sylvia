from citation_graph import CitationGraph

def test_citation_graph():
    cg = CitationGraph()
    cg.add_paper("p1", ["p2", "p3"])
    assert cg.get_citations("p1") == ["p2", "p3"]
