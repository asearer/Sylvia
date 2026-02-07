# classifier/tests/test_dataset.py

import sys
from pathlib import Path

# Add the src directory to the Python path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from dataset import load_synthetic_dataset

def test_synthetic_dataset_shape():
    X, y = load_synthetic_dataset(n_samples=100)
    assert X.shape == (100, 10)
    assert y.shape == (100,)