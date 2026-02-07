# classifier/src/config.py
"""
Configuration management for the classifier service.
Provides:
- Typed config class
- Automatic env loading
- Override support
"""

from dataclasses import dataclass
import os
from dotenv import load_dotenv

load_dotenv()


@dataclass
class MatrixConfig:
    homeserver: str
    user: str
    password: str
    room_id: str


@dataclass
class TrainingConfig:
    epochs: int = 5
    learning_rate: float = 0.001
    batch_size: int = 32
    seed: int = 42


@dataclass
class ClassifierConfig:
    matrix: MatrixConfig
    training: TrainingConfig


def load_config() -> ClassifierConfig:
    """Loads configuration from environment variables."""
    matrix = MatrixConfig(
        homeserver=os.getenv("MATRIX_HOMESERVER", ""),
        user=os.getenv("MATRIX_USER", ""),
        password=os.getenv("MATRIX_PASSWORD", ""),
        room_id=os.getenv("MATRIX_ROOM_ID", "")
    )

    training = TrainingConfig(
        epochs=int(os.getenv("TRAIN_EPOCHS", 5)),
        learning_rate=float(os.getenv("TRAIN_LR", 0.001)),
        batch_size=int(os.getenv("TRAIN_BATCH", 32)),
        seed=int(os.getenv("TRAIN_SEED", 42)),
    )

    return ClassifierConfig(matrix=matrix, training=training)
