import streamlit as st
from unittest.mock import patch
import sys
from pathlib import Path

# Add the src directory to the Python path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from interface import render_code_analyzer

def test_code_analysis_calls_service(mocker):
    st.session_state.clear()
    st.session_state["Analyze Code"] = True

    mocker.patch("streamlit.text_area", return_value="print('hello')")
    mocker.patch("streamlit.button", return_value=True)
    mock_analyze = mocker.patch(
        "interface.analyze_code",
        return_value="SAFE"
    )

    render_code_analyzer()

    mock_analyze.assert_called_once_with("print('hello')")