from event_handler import EventHandler
from message_router import MessageRouter
from discord_client import DiscordClient
from matrix_client import MatrixClient

def test_event_handler_listen():
    discord = DiscordClient()
    matrix = MatrixClient()
    router = MessageRouter([discord, matrix])
    handler = EventHandler(router)
    discord.connect()
    matrix.connect()
    handler.listen()
