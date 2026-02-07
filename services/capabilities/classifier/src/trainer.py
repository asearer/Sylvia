# classifier/src/trainer.py
"""
The main training loop with metric reporting.
"""

import numpy as np
from .model import LogisticClassifier
from .metrics import MetricState
from .dataset import load_synthetic_dataset
from .reporting import Reporter


class Trainer:

    def __init__(self, config):
        self.config = config
        self.reporter = Reporter(config)

    def train(self):
        X, y = load_synthetic_dataset()
        model = LogisticClassifier(lr=self.config.training.learning_rate)
        model.initialize(X.shape[1])

        for epoch in range(1, self.config.training.epochs + 1):
            loss = model.train_step(X, y)
            preds = model.predict(X)
            accuracy = np.mean(preds == y)

            metrics = MetricState(epoch, loss, accuracy)
            self.reporter.report(metrics)
