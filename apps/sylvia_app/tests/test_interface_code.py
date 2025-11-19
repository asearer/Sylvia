import streamlit as st
from unittest.mock import patch

from apps.sylvia_app.src.interface import render_code_analyzer

def test_code_analysis_calls_service(mocker):
    st.session_state.clear()
    st.session_state["Analyze Code"] = True

    mocker.patch("streamlit.text_area", return_value="print('hello')")
    mock_analyze = mocker.patch(
        "apps.sylvia_app.src.interface.analyze_code",
        return_value="SAFE"
    )

    render_code_analyzer()

    mock_analyze.assert_called_once_with("print('hello')")
