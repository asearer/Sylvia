import pytest
import sys
from pathlib import Path

# Add the parent directory to the Python path
sys.path.insert(0, str(Path(__file__).parent.parent))

from matrix_adapter import MatrixAdapter

def test_matrix_adapter_instantiation():
    adapter = MatrixAdapter(token="dummy")
    assert adapter.token == "dummy"