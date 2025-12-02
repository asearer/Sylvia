import pytest
from unittest.mock import patch, MagicMock
import streamlit as st
import sys
from pathlib import Path

# Add the src directory to the Python path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from interface import (
    push_alert_to_chat,
    render_chat
)

@pytest.fixture(autouse=True)
def reset_session_state():
    st.session_state.clear()
    st.session_state.chat_history = []
    yield


def test_push_alert_to_chat_adds_message():
    push_alert_to_chat("Camera detected motion", alert_type="camera")

    assert len(st.session_state.chat_history) == 1
    entry = st.session_state.chat_history[0]
    assert entry["message"] == "Camera detected motion"
    assert entry["type"] == "camera"
    assert "actions" in entry


def test_render_chat_user_message_triggers_response(mocker):
    # Mock Sylvia personality engine
    mock_process = mocker.patch(
        "interface.process_message",
        return_value="Hello user!"
    )

    # Set fake user message
    st.session_state.chat_history = []
    st.session_state["chat_input"] = "Hello Sylvia"

    # Run chat render
    mocker.patch("streamlit.button", return_value=True)
    mocker.patch("streamlit.text_input", return_value="Hello Sylvia")
    render_chat()

    mock_process.assert_called_once_with("Hello Sylvia")