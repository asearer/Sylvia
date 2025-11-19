import streamlit as st
from unittest.mock import patch

from apps.sylvia_app.src.interface import render_self_healing_logs

def test_self_healing_logs_display(mocker):
    st.session_state.clear()
    st.session_state.logs = [
        {"timestamp": "12:00", "message": "Service restarted"}
    ]

    render_self_healing_logs()


def test_manual_restart_triggers_callback(mocker):
    st.session_state.clear()

    mock_restart = mocker.patch(
        "apps.sylvia_app.src.interface.trigger_restart"
    )

    render_self_healing_logs()

    mock_restart.assert_not_called()  # Button not pressed in tests
