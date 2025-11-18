"""
Routes messages between services and integrations.
"""

class MessageRouter:
    def __init__(self, clients):
        self.clients = clients

    def route_message(self, source, message):
        """
        Route message to other clients.
        """
        for client in self.clients:
            if client != source:
                client.send_message("default_channel", message["content"])
