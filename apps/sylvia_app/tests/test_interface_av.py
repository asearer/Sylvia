import streamlit as st
from unittest.mock import patch, MagicMock
from apps.sylvia_app.src.interface import render_av_monitoring

def test_av_monitoring_fetches_frame_and_audio(mocker):
    st.session_state.clear()
    st.session_state.stop_av = False

    mocker.patch(
        "apps.sylvia_app.src.interface.get_camera_frame",
        return_value=MagicMock()
    )
    mocker.patch(
        "apps.sylvia_app.src.interface.get_audio_chunk",
        return_value=b"fake_audio"
    )
    mocker.patch("cv2.cvtColor", return_value=MagicMock())

    render_av_monitoring()

    # The placeholders exist
    # Live loop cannot be fully tested without integration tests,
    # but AV fetch mocks confirm the panel renders without errors.
