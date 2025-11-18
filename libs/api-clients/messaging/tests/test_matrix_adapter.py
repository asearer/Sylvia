import pytest
from matrix_adapter import MatrixAdapter

def test_matrix_adapter_instantiation():
    adapter = MatrixAdapter(token="dummy")
    assert adapter.token == "dummy"
