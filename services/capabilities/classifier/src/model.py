# classifier/src/model.py
"""
Simple logistic regression implemented in NumPy.
"""

import numpy as np


class LogisticClassifier:

    def __init__(self, lr: float = 0.001):
        self.lr = lr
        self.weights = None

    def _sigmoid(self, x):
        return 1 / (1 + np.exp(-x))

    def predict_proba(self, X):
        return self._sigmoid(X @ self.weights)

    def predict(self, X):
        return (self.predict_proba(X) >= 0.5).astype(int)

    def initialize(self, n_features: int):
        self.weights = np.zeros(n_features)

    def train_step(self, X, y):
        preds = self.predict_proba(X)
        error = preds - y
        grad = X.T @ error / len(X)
        self.weights -= self.lr * grad

        # Loss (binary cross entropy)
        loss = -np.mean(y * np.log(preds + 1e-8) + (1 - y) * np.log(1 - preds + 1e-8))
        return loss
