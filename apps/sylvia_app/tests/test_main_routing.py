import streamlit as st
from unittest.mock import patch
import sys
from pathlib import Path

# Add the src directory to the Python path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

import main
import importlib

def test_main_routing_chat(mocker):
    mocker.patch("streamlit.sidebar.radio", return_value="Chat")
    mock_chat = mocker.patch("interface.render_chat")

    importlib.reload(main)

    mock_chat.assert_called_once()


def test_main_routing_voice(mocker):
    mocker.patch("streamlit.sidebar.radio", return_value="Voice Assistant")
    mock_voice = mocker.patch("interface.render_voice_assistant")

    importlib.reload(main)

    mock_voice.assert_called_once()