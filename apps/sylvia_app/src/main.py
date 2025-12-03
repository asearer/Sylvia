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

# Add project root to sys.path to allow importing 'services'
# We need to go up 4 levels: src -> sylvia_app -> apps -> Sylvia (Root)
project_root = Path(__file__).resolve().parent.parent.parent.parent
if str(project_root) not in sys.path:
    sys.path.append(str(project_root))

import streamlit as st
from interface import (
    render_chat,
    render_voice_assistant,
    render_av_monitoring,
    render_code_analyzer,
    render_self_healing_logs
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
# Sidebar: Global Controls & Status
# ----------------------------------------------------------------------
st.sidebar.title("Sylvia System")
if st.sidebar.button("Refresh System"):
    st.rerun()

st.sidebar.markdown("---")
st.sidebar.info("System Status: Online")

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
    
    # Other tools are organized in tabs to save space but remain accessible
    tab1, tab2, tab3 = st.tabs(["Voice", "Code", "Logs"])
    
    with tab1:
        render_voice_assistant()
        
    with tab2:
        render_code_analyzer()
        
    with tab3:
        render_self_healing_logs()
