import streamlit as st
from unittest.mock import patch

from apps.sylvia_app.src import main

def test_main_routing_chat(mocker):
    mocker.patch("streamlit.sidebar.radio", return_value="Chat")
    mock_chat = mocker.patch("apps.sylvia_app.src.main.render_chat")

    main

    mock_chat.assert_called_once()


def test_main_routing_voice(mocker):
    mocker.patch("streamlit.sidebar.radio", return_value="Voice Assistant")
    mock_voice = mocker.patch("apps.sylvia_app.src.main.render_voice_assistant")

    main

    mock_voice.assert_called_once()
