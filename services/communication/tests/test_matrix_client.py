from matrix_client import MatrixClient

def test_matrix_send_receive():
    client = MatrixClient()
    client.connect()
    client.send_message("lobby", "Test")
    msg = client.receive_message()
    assert "content" in msg
