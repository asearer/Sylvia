"""
Entrypoint for the Communication service.
Coordinates Discord, Matrix, and other integrations.
"""

from discord_client import DiscordClient
from matrix_client import MatrixClient
from message_router import MessageRouter
from event_handler import EventHandler

class CommunicationService:
    def __init__(self):
        self.discord = DiscordClient()
        self.matrix = MatrixClient()
        self.router = MessageRouter([self.discord, self.matrix])
        self.event_handler = EventHandler(self.router)

    def start(self):
        """
        Start listening and routing messages.
        """
        self.discord.connect()
        self.matrix.connect()
        self.event_handler.listen()

if __name__ == "__main__":
    service = CommunicationService()
    service.start()
