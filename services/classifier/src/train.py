"""
Example ML training script with Matrix event sending

1. Set Matrix credentials (see below, use env/config in practice)
2. Run training loop (dummy example)
3. Send metrics (accuracy, loss, epoch) to Matrix room after each epoch

Install dependencies for this script:
    pip install matrix-nio[http]
"""
import time
import random
from libs.api-clients.matrix_wrapper import MatrixClientSync

# TODO: For production, use secure config/env variables not hardcoded values!
MATRIX_HOMESERVER = "https://matrix.org"   # e.g., "https://your-hs"
MATRIX_BOT_USER = "@botuser:matrix.org"
MATRIX_BOT_PASSWORD = "yourpassword"
MATRIX_ROOM_ID = "!yourroomid:matrix.org"

NUM_EPOCHS = 5

def train_and_report():
    client = MatrixClientSync(MATRIX_HOMESERVER, MATRIX_BOT_USER, MATRIX_BOT_PASSWORD, MATRIX_ROOM_ID)
    accuracy = 0.75
    loss = 1.0
    for epoch in range(1, NUM_EPOCHS+1):
        # Simulate metrics changing
        accuracy += random.uniform(0.01, 0.05)
        loss -= random.uniform(0.05, 0.2)
        metrics = {"epoch": epoch, "accuracy": round(accuracy, 4), "loss": round(loss, 4)}
        print(f"[Epoch {epoch}] Sending metrics to Matrix: {metrics}")
        client.send_ml_metrics(metrics)
        time.sleep(2)

if __name__ == "__main__":
    train_and_report()
