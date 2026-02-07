# classifier/tests/fixtures/mock_dataset.py

import numpy as np

def mock_dataset():
    np.random.seed(42)
    X = np.random.randn(20, 10)
    y = (X[:, 0] > 0).astype(int)
    return X, y
