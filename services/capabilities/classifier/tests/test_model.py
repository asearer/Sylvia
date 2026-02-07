# classifier/tests/test_model.py

import numpy as np
import sys
from pathlib import Path

# Add the src directory to the Python path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from model import LogisticClassifier

def test_logistic_model_training_step():
    X = np.random.randn(50, 10)
    y = (X[:, 0] > 0).astype(int)

    model = LogisticClassifier(lr=0.1)
    model.initialize(X.shape[1])

    initial_weights = model.weights.copy()
    loss = model.train_step(X, y)

    assert loss > 0
    assert not np.allclose(initial_weights, model.weights)