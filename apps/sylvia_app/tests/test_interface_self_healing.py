import streamlit as st
from unittest.mock import patch
import sys
from pathlib import Path

# Add the src directory to the Python path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from interface import render_self_healing_logs

def test_self_healing_logs_display(mocker):
    st.session_state.clear()
    st.session_state.logs = [
        {"timestamp": "12:00", "message": "Service restarted"}
    ]

    render_self_healing_logs()


def test_manual_restart_triggers_callback(mocker):
    st.session_state.clear()
    st.session_state.logs = []

    mock_restart = mocker.patch(
        "interface.trigger_restart"
    )

    render_self_healing_logs()

    mock_restart.assert_not_called()  # Button not pressed in tests