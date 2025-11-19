class MockChatService:
    """Mock chat service to simulate conversation logic."""
    def __init__(self):
        self.messages = []

    def send_message(self, message: str) -> str:
        self.messages.append(message)
        return f"Mock response to: {message}"

    def get_history(self):
        return self.messages
