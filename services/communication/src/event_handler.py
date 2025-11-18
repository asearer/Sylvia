"""
Listens to messages and triggers appropriate events.
"""

class EventHandler:
    def __init__(self, router):
        self.router = router

    def listen(self):
        """
        Placeholder event loop to simulate message listening.
        """
        # In production, would use async event loops
        for client in self.router.clients:
            msg = client.receive_message()
            self.router.route_message(client, msg)
            print(f"Routed message: {msg}")
