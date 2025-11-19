# classifier/tests/fixtures/mock_config.py

from classifier.src.config import MatrixConfig, TrainingConfig, ClassifierConfig


def get_mock_config():
    return ClassifierConfig(
        matrix=MatrixConfig(
            homeserver="mock://server",
            user="@test:server",
            password="pass",
            room_id="!room:server"
        ),
        training=TrainingConfig(
            epochs=3,
            learning_rate=0.1,
            batch_size=16,
            seed=123
        )
    )
