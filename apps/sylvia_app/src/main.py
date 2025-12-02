"""
Sylvia App Entrypoint (Streamlit).

This module launches the Streamlit frontend for Sylvia and provides:
1. Sidebar navigation between features:
    - Chat
    - Voice Assistant
    - Live A/V Monitoring
    - Code Analyzer
    - Self-Healing / System Logs
2. Status refresh functionality
3. Central orchestration of all interactive panels

Usage:
    streamlit run apps/sylvia_app/src/main.py
"""

import streamlit as st
from interface import (
    render_chat,
    render_voice_assistant,
    render_av_monitoring,
    render_code_analyzer,
    render_self_healing_logs
)

# ----------------------------------------------------------------------
# Sidebar: Feature Selection
# ----------------------------------------------------------------------
st.sidebar.title("Sylvia Controls")

# Radio button menu for selecting the feature panel
feature = st.sidebar.radio(
    "Select Feature",
    ["Chat", "Voice Assistant", "A/V Monitoring", "Code Analyzer", "Self-Healing Logs"]
)

# Button to refresh the current status (rerun Streamlit)
if st.sidebar.button("Refresh Status"):
    st.rerun()

# ----------------------------------------------------------------------
# Main Content: Render selected feature
# ----------------------------------------------------------------------
if feature == "Chat":
    # Interactive chat with alerts, emojis, colors, and action buttons
    render_chat()
elif feature == "Voice Assistant":
    # Voice input/output panel
    render_voice_assistant()
elif feature == "A/V Monitoring":
    # Live camera/audio monitoring panel
    render_av_monitoring()
elif feature == "Code Analyzer":
    # DeepHat-powered code analysis panel
    render_code_analyzer()
elif feature == "Self-Healing Logs":
    # Display system/self-healing logs and restart controls
    render_self_healing_logs()
