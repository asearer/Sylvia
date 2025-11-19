# classifier/src/dataset.py
"""
Dataset loader abstraction.
Allows swapping synthetic, local, or remote datasets.
"""

import numpy as np
from typing import Tuple


def load_synthetic_dataset(n_samples=500) -> Tuple[np.ndarray, np.ndarray]:
    """
    Generates a synthetic binary classification dataset.
    Returns X (features) and y (labels).
    """
    X = np.random.randn(n_samples, 10)
    y = (X[:, 0] + X[:, 1] * 0.5 > 0).astype(int)
    return X, y
