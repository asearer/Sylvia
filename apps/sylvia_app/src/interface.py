"""
Sylvia Frontend Interface (Streamlit)
-------------------------------------
This module provides the interactive Streamlit frontend for Sylvia. It integrates:
1. Chat interface with color-coded messages and emojis.
2. Contextual action buttons for alerts (camera, audio, system, self-healing).
3. Voice assistant input/output.
4. Live audio/video monitoring.
5. Code analysis using DeepHat-powered analyzer.
6. Self-healing log display and service control.

"""

"""
Sylvia App Interface Module.

This module defines the Streamlit UI components for the Sylvia application.
It handles the rendering of various panels such as Chat, Voice Assistant,
A/V Monitoring, Code Analysis, and Self-Healing Logs.

It interacts with backend services via direct imports (currently) and manages
session state for interactive elements.
"""

import streamlit as st
import cv2
import threading
import time
import numpy as np
from datetime import datetime

# Import Sylvia service modules
from services.personality_engine.src.engine import process_message
from services.voice_assistant.src.speech_to_text import transcribe_audio
from services.voice_assistant.src.text_to_speech import synthesize_speech
from services.sensor_input.camera.src.main import get_camera_frame, get_activity_alerts, record_clip
from services.sensor_input.audio.src.main import get_audio_chunk, get_audio_alerts, save_audio
from services.code_analysis.src.analyzer import analyze_code
from services.self_healing.src.monitor import get_system_logs, trigger_restart, subscribe_to_events

# ----------------------------------------------------------------------
# Session State Initialization
# ----------------------------------------------------------------------
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []  # Stores all chat messages and alerts
if "av_status" not in st.session_state:
    st.session_state.av_status = "Idle"  # Status of live A/V monitoring
if "stop_av" not in st.session_state:
    st.session_state.stop_av = False  # Flag to stop A/V monitoring threads
if "logs" not in st.session_state:
    st.session_state.logs = []  # Stores system/self-healing logs
if "alerts_thread_started" not in st.session_state:
    st.session_state.alerts_thread_started = False  # Ensures background thread starts once

# ----------------------------------------------------------------------
# Function: push_alert_to_chat
# ----------------------------------------------------------------------
def push_alert_to_chat(alert_message: str, alert_type: str = "system"):
    """
    Push a new alert or system message into the chat panel with contextual action buttons.

    Args:
        alert_message (str): The content of the alert/message.
        alert_type (str): Type of alert; determines color coding and actions.
                          Options: "camera", "audio", "self_healing", "system", "chat_response".
    """
    actions = []

    # Define contextual actions per alert type
    if alert_type == "camera":
        actions = [
            {"label": "Acknowledge", "callback": lambda: None},
            {"label": "Mute Camera Alerts", "callback": lambda: push_alert_to_chat("Camera alerts muted.", "system")},
            {"label": "Record Clip", "callback": lambda: record_clip()}
        ]
    elif alert_type == "audio":
        actions = [
            {"label": "Acknowledge", "callback": lambda: None},
            {"label": "Mute Audio Alerts", "callback": lambda: push_alert_to_chat("Audio alerts muted.", "system")},
            {"label": "Save Audio", "callback": lambda: save_audio()}
        ]
    elif alert_type == "self_healing":
        actions = [
            {"label": "Acknowledge", "callback": lambda: None},
            {"label": "Trigger Restart", "callback": trigger_restart},
            {"label": "Investigate", "callback": lambda: push_alert_to_chat("Investigation started...", "system")}
        ]
    elif alert_type == "system":
        actions = [{"label": "Acknowledge", "callback": lambda: None}]
    else:
        actions = []

    # Append to chat history
    st.session_state.chat_history.append({
        "message": alert_message,
        "is_user": False,
        "type": alert_type,
        "actions": actions
    })

    # Trigger UI rerun to reflect new message
    st.rerun()

# ----------------------------------------------------------------------
# Function: start_alerts_listener
# ----------------------------------------------------------------------
def start_alerts_listener():
    """
    Start a background thread that listens for:
    - System/self-healing events (via subscribe_to_events)
    - Camera motion/activity alerts
    - Audio alerts

    Alerts are pushed to the chat panel in real time with contextual actions.
    """
    def alerts_loop():
        # Self-healing/system events
        for event in subscribe_to_events():
            st.session_state.logs.append(event)
            push_alert_to_chat(event['message'], alert_type="self_healing")
            time.sleep(0.1)

        # Continuous camera/audio monitoring
        while True:
            cam_alert = get_activity_alerts()
            if cam_alert:
                push_alert_to_chat(cam_alert, "camera")

            audio_alert = get_audio_alerts()
            if audio_alert:
                push_alert_to_chat(audio_alert, "audio")

            time.sleep(1)

    threading.Thread(target=alerts_loop, daemon=True).start()

# Start the alert listener once
if not st.session_state.alerts_thread_started:
    start_alerts_listener()
    st.session_state.alerts_thread_started = True

# ----------------------------------------------------------------------
# Function: render_chat
# ----------------------------------------------------------------------
def render_chat():
    """
    Render the interactive chat panel:
    - Displays all messages (user, chat responses, alerts)
    - Color-coded by message type
    - Renders action buttons for contextual alerts
    - Allows sending user messages
    """
    st.header("💬 Chat with Sylvia")

    for idx, entry in enumerate(st.session_state.chat_history):
        msg_type = entry.get("type", "chat_response")
        is_user = entry.get("is_user", False)
        actions = entry.get("actions", [])
        msg = entry["message"]

        # Color mapping for message types
        color_map = {
            "system": "orange",
            "camera": "blue",
            "audio": "purple",
            "self_healing": "red",
            "chat_response": "green",
            "user": "black"
        }
        color = color_map.get(msg_type, "black")
        st.markdown(f"<span style='color:{color}'>{msg}</span>", unsafe_allow_html=True)

        # Render action buttons dynamically
        for action in actions:
            if st.button(action["label"], key=f"{idx}_{action['label']}"):
                action["callback"]()  # Execute callback
                st.success(f"Action '{action['label']}' executed!")

    # Input for user messages
    user_input = st.text_input("Type your message...", key="chat_input")
    if st.button("Send") and user_input:
        st.session_state.chat_history.append({
            "message": user_input,
            "is_user": True,
            "type": "user"
        })
        response = process_message(user_input)
        push_alert_to_chat(response, alert_type="chat_response")

# ----------------------------------------------------------------------
# Function: render_voice_assistant
# ----------------------------------------------------------------------
def render_voice_assistant():
    """
    Render the Voice Assistant panel:
    - Upload audio file for transcription
    - Process voice input
    - Outputs chat response and audio synthesis
    """
    st.header("🎙️ Voice Assistant")
    audio_file = st.file_uploader("Upload audio file", type=["wav", "mp3"])

    if st.button("Process Voice Input") and audio_file:
        text = transcribe_audio(audio_file)
        response = process_message(text)
        push_alert_to_chat(response, alert_type="chat_response")
        st.audio(synthesize_speech(response))

# ----------------------------------------------------------------------
# Function: render_av_monitoring
# ----------------------------------------------------------------------
def render_av_monitoring():
    """
    Render Live Audio/Video Monitoring panel:
    - Displays live camera feed
    - Streams live audio chunks
    - Uses background thread for continuous updates
    """
    st.header("📹 Live Audio/Video Monitoring")
    st.write(f"Feed status: {st.session_state.av_status}")
    video_placeholder = st.empty()
    audio_placeholder = st.empty()

    def av_loop():
        while not st.session_state.stop_av:
            frame = get_camera_frame()
            if frame is not None:
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                video_placeholder.image(frame, channels="RGB")

            audio_bytes = get_audio_chunk()
            if audio_bytes:
                audio_placeholder.audio(audio_bytes, format="audio/wav")
            time.sleep(0.1)

    if st.button("Start Live Monitoring"):
        st.session_state.av_status = "Active"
        st.session_state.stop_av = False
        threading.Thread(target=av_loop, daemon=True).start()

    if st.button("Stop Live Monitoring"):
        st.session_state.stop_av = True
        st.session_state.av_status = "Idle"

# ----------------------------------------------------------------------
# Function: render_code_analyzer
# ----------------------------------------------------------------------
def render_code_analyzer():
    """
    Render the Code Analyzer panel:
    - Accepts pasted code input
    - Runs DeepHat-powered code analysis
    - Displays results
    """
    st.header("🖥️ Code Understanding / Analysis")
    code_input = st.text_area("Paste your code here")
    if st.button("Analyze Code") and code_input.strip():
        result = analyze_code(code_input)
        st.code(result)

# ----------------------------------------------------------------------
# Function: render_self_healing_logs
# ----------------------------------------------------------------------
def render_self_healing_logs():
    """
    Render the Self-Healing Logs panel:
    - Displays latest system/self-healing logs
    - Allows triggering manual service restart
    """
    st.header("⚡ Self-Healing / System Logs")
    log_placeholder = st.empty()

    if st.session_state.logs:
        with log_placeholder.container():
            for log in st.session_state.logs[-20:]:
                st.markdown(f"<span style='color:red'>{log['timestamp']} - {log['message']}</span>", unsafe_allow_html=True)

    if st.button("Trigger Restart"):
        trigger_restart()
        push_alert_to_chat("Manual restart triggered", "self_healing")
        st.success("Restart command sent!")
