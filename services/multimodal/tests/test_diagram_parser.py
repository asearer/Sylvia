from diagram_parser import DiagramParser

def test_parse():
    parser = DiagramParser()
    result = parser.parse("sample.png")
    assert isinstance(result, list)
