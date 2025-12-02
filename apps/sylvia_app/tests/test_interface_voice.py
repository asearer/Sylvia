import streamlit as st
from unittest.mock import patch, MagicMock
import sys
from pathlib import Path

# Add the src directory to the Python path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from interface import render_voice_assistant

def test_voice_assistant_pipeline(mocker):
    st.session_state.clear()
    st.session_state.chat_history = []

    mock_file = MagicMock()
    mocker.patch("streamlit.file_uploader", return_value=mock_file)

    mock_transcribe = mocker.patch(
        "interface.transcribe_audio",
        return_value="Turn on the lights"
    )

    mock_process = mocker.patch(
        "interface.process_message",
        return_value="Lights turned on"
    )

    mock_tts = mocker.patch(
        "interface.synthesize_speech",
        return_value=b'FAKE_AUDIO_BYTES'
    )

    mocker.patch("streamlit.button", return_value=True)
    render_voice_assistant()

    mock_transcribe.assert_called_once()
    mock_process.assert_called_once_with("Turn on the lights")
    mock_tts.assert_called_once_with("Lights turned on")