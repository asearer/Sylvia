"""
Sylvia App Entrypoint (Streamlit).

This module launches the Streamlit frontend for Sylvia and provides:
1. Unified Dashboard Layout:
    - Chat (Left Column)
    - A/V Monitoring & Tools (Right Column)
2. Central orchestration of all interactive panels

Usage:
    streamlit run apps/sylvia_app/src/main.py
"""

import sys
import os
from pathlib import Path
import logging

# Configure logging immediately to capture import-time logs
logging.basicConfig(level=logging.INFO)

# Add project root to sys.path to allow importing 'services'
# We need to go up 4 levels: src -> sylvia_app -> apps -> Sylvia (Root)
project_root = Path(__file__).resolve().parent.parent.parent.parent
if str(project_root) not in sys.path:
    sys.path.append(str(project_root))

import streamlit as st
from interface import (
    render_sidebar,
    render_chat,
    render_voice_assistant,
    render_av_monitoring,
    render_code_analyzer,
    render_system_health_and_logs,
    initialize_session_state,
    start_background_threads
)

# ----------------------------------------------------------------------
# Page Configuration
# ----------------------------------------------------------------------
st.set_page_config(
    page_title="Sylvia Dashboard",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ----------------------------------------------------------------------
# Initialization
# ----------------------------------------------------------------------
initialize_session_state()
start_background_threads()

# ----------------------------------------------------------------------
# Custom CSS for VSCode Aesthetic
# ----------------------------------------------------------------------
st.markdown("""
<style>
    /* Global Font */
    html, body, [class*="css"] {
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    
    /* Remove rounded corners from buttons and inputs */
    .stButton > button {
        border-radius: 0px;
        border: 1px solid #3e3e42;
        background-color: #0e639c;
        color: white;
    }
    .stButton > button:hover {
        background-color: #1177bb;
        border-color: #3e3e42;
    }
    .stTextInput > div > div > input {
        border-radius: 0px;
        background-color: #3c3c3c;
        color: #cccccc;
        border: 1px solid #3c3c3c;
    }
    
    /* Sidebar styling */
    section[data-testid="stSidebar"] {
        background-color: #252526;
    }
    
    /* Tabs styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 2px;
        background-color: #252526;
    }
    .stTabs [data-baseweb="tab"] {
        border-radius: 0px;
        background-color: #2d2d2d;
        color: #969696;
        padding: 4px 16px;
    }
    .stTabs [aria-selected="true"] {
        background-color: #1e1e1e;
        color: white;
        border-top: 1px solid #007acc;
    }
    
    /* Reduce padding for a denser "IDE" feel */
    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
    }
</style>
""", unsafe_allow_html=True)

# ----------------------------------------------------------------------
# Sidebar
# ----------------------------------------------------------------------
render_sidebar()

# ----------------------------------------------------------------------
# Main Content: Unified Grid Layout
# ----------------------------------------------------------------------

# Create two main columns
left_col, right_col = st.columns([0.6, 0.4], gap="medium")

with left_col:
    # Chat is the primary interface
    render_chat()

with right_col:
    # A/V Monitoring is always visible at the top
    render_av_monitoring()
    
    st.markdown("---")
    
    # Other tools are organized in blocks
    st.markdown("### Voice Assistant")
    render_voice_assistant()
    
    st.markdown("---")
    
    st.markdown("### Code Analyzer")
    render_code_analyzer()
    
    st.markdown("---")
    
    render_system_health_and_logs()
