from main import CommunicationService

def test_service_start():
    service = CommunicationService()
    service.discord.connect()
    service.matrix.connect()
    assert service.discord.connected
    assert service.matrix.connected
