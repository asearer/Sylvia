from query_processor import QueryProcessor

def test_process_query():
    qp = QueryProcessor()
    result = qp.process("Test query")
    assert "Test query" in result
