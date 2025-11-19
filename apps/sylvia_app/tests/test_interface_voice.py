import streamlit as st
from unittest.mock import patch, MagicMock

from apps.sylvia_app.src.interface import render_voice_assistant

def test_voice_assistant_pipeline(mocker):
    st.session_state.clear()

    mock_file = MagicMock()
    mocker.patch("streamlit.file_uploader", return_value=mock_file)

    mock_transcribe = mocker.patch(
        "apps.sylvia_app.src.interface.transcribe_audio",
        return_value="Turn on the lights"
    )

    mock_process = mocker.patch(
        "apps.sylvia_app.src.interface.process_message",
        return_value="Lights turned on"
    )

    mock_tts = mocker.patch(
        "apps.sylvia_app.src.interface.synthesize_speech",
        return_value=b'FAKE_AUDIO_BYTES'
    )

    render_voice_assistant()

    mock_transcribe.assert_called_once()
    mock_process.assert_called_once_with("Turn on the lights")
    mock_tts.assert_called_once_with("Lights turned on")
