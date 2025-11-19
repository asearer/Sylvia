# classifier/tests/fixtures/mock_matrix_client.py

class MockMatrixClient:
    def __init__(self):
        self.sent_messages = []

    def send_ml_metrics(self, payload):
        self.sent_messages.append(payload)
