from discord_client import DiscordClient

def test_discord_send_receive():
    client = DiscordClient()
    client.connect()
    client.send_message("general", "Test")
    msg = client.receive_message()
    assert "content" in msg
