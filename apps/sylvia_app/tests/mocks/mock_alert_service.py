class MockAlertService:
    """Mock internal alert + event routing."""
    def __init__(self):
        self.events = []

    def send_alert(self, title: str, payload: dict):
        event = {"title": title, "payload": payload}
        self.events.append(event)
        return event
