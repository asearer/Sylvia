from message_router import MessageRouter
from discord_client import DiscordClient
from matrix_client import MatrixClient

def test_route_message():
    discord = DiscordClient()
    matrix = MatrixClient()
    router = MessageRouter([discord, matrix])
    message = {"content": "Hello"}
    router.route_message(discord, message)
