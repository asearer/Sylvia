# classifier/src/train.py
"""
Classifier service entrypoint.
Loads configuration, initializes trainer, and starts training loop.
"""

from config import load_config
from trainer import Trainer


def main():
    config = load_config()
    trainer = Trainer(config)
    trainer.train()


if __name__ == "__main__":
    main()
