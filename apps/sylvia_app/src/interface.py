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
import cv2
import numpy as np
import pandas as pd
from datetime import datetime

# Import Sylvia service modules
from services.personality_engine.src.engine import process_message, set_llm_provider, get_analytics_data, set_system_prompt
from services.voice_assistant.src.speech_to_text import transcribe_audio
from services.voice_assistant.src.text_to_speech import synthesize_speech
from services.sensor_input.camera.src.main import get_camera_frame, get_activity_alerts, record_clip, list_cameras, detect_objects_in_frame
from services.sensor_input.audio.src.main import get_audio_chunk, get_audio_alerts, save_audio, get_audio_visualizer_data
from services.code_analysis.src.analyzer import analyze_code
from services.self_healing.src.monitor import get_system_logs, trigger_restart, subscribe_to_events, get_system_metrics

# ----------------------------------------------------------------------
# Session State Initialization
# ----------------------------------------------------------------------
# ----------------------------------------------------------------------
# Session State Initialization
# ----------------------------------------------------------------------
def initialize_session_state():
    """Initialize Streamlit session state variables if they don't exist."""
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

import queue

# Global queue for thread-safe alert handling
alert_queue = queue.Queue()

# ----------------------------------------------------------------------
# Function: start_alerts_listener
# ----------------------------------------------------------------------
def start_alerts_listener():
    """
    Start a background thread that listens for:
    - System/self-healing events (via subscribe_to_events)
    - Camera motion/activity alerts
    - Audio alerts

    Alerts are put into a thread-safe queue to be processed by the main thread.
    """
    def alerts_loop():
        # Self-healing/system events
        for event in subscribe_to_events():
            alert_queue.put({"type": "self_healing", "payload": event})
            time.sleep(0.1)

        # Continuous camera/audio monitoring
        while True:
            cam_alert = get_activity_alerts()
            if cam_alert:
                alert_queue.put({"type": "camera", "payload": cam_alert})

            audio_alert = get_audio_alerts()
            if audio_alert:
                alert_queue.put({"type": "audio", "payload": audio_alert})

            time.sleep(1)

    threading.Thread(target=alerts_loop, daemon=True).start()

# ----------------------------------------------------------------------
# Function: start_background_threads
# ----------------------------------------------------------------------
def start_background_threads():
    """
    Start background threads for alerts and monitoring.
    Should be called after session state initialization.
    """
    if not st.session_state.alerts_thread_started:
        start_alerts_listener()
        st.session_state.alerts_thread_started = True

# ----------------------------------------------------------------------
# Function: render_sidebar
# ----------------------------------------------------------------------
def render_sidebar():
    """
    Render the global sidebar with settings and controls.
    """
    with st.sidebar:
        st.title("Sylvia Control")
        
        # Model Settings
        with st.expander("Model Settings", expanded=False):
            provider = st.selectbox("LLM Provider", ["Local (DistilGPT2)", "Gemini", "OpenAI", "Anthropic"])
            api_key = ""
            if provider != "Local (DistilGPT2)":
                api_key = st.text_input(f"{provider} API Key", type="password")
            
            if st.button("Update Model"):
                # Map selection to internal names
                provider_map = {
                    "Local (DistilGPT2)": "Local",
                    "Gemini": "Gemini",
                    "OpenAI": "OpenAI",
                    "Anthropic": "Anthropic"
                }
                set_llm_provider(provider_map[provider], api_key)
                st.success(f"Switched to {provider}")

        # Personality Settings
        with st.expander("Personality Settings", expanded=False):
            presets = {
                "Professional": "You are Sylvia, a helpful, professional, and concise AI assistant.",
                "Friendly": "You are Sylvia, a warm, friendly, and enthusiastic AI companion. You use emojis and casual language.",
                "Sarcastic": "You are Sylvia. You are helpful but extremely sarcastic and dry. You like to make witty observations.",
                "Coder": "You are Sylvia, an expert software engineer. You focus on code quality, best practices, and technical details. You are concise.",
                "Custom": ""
            }
            
            preset_name = st.selectbox("Personality Preset", list(presets.keys()))
            
            # Initialize session state for custom prompt if not exists
            if "system_prompt" not in st.session_state:
                st.session_state.system_prompt = presets["Professional"]
            
            # Update prompt text based on preset selection (if not custom)
            if preset_name != "Custom":
                st.session_state.system_prompt = presets[preset_name]

            system_prompt = st.text_area("System Prompt", value=st.session_state.system_prompt, height=100)
            
            if st.button("Update Personality"):
                set_system_prompt(system_prompt)
                st.session_state.system_prompt = system_prompt # Sync state
                st.success(f"Personality updated to {preset_name}")

        st.markdown("---")
        if st.button("Clear Chat History"):
            st.session_state.chat_history = []
            st.rerun()

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
@st.fragment(run_every=0.1)
def render_av_monitoring():
    """
    Render the A/V Monitoring panel.
    """
    st.subheader("Live A/V Monitoring")
    
    # Process alerts from queue
    try:
        while True:
            alert = alert_queue.get_nowait()
            if alert["type"] == "self_healing":
                st.session_state.logs.append(alert["payload"])
                push_alert_to_chat(alert["payload"]["message"], alert_type="self_healing")
            elif alert["type"] == "camera":
                push_alert_to_chat(alert["payload"], alert_type="camera")
            elif alert["type"] == "audio":
                push_alert_to_chat(alert["payload"], alert_type="audio")
    except queue.Empty:
        pass
    
    # Camera Controls
    col_cam1, col_cam2, col_cam3 = st.columns([1, 1, 2])
    with col_cam1:
        camera_power = st.toggle("Camera Power", value=True)
    with col_cam2:
        object_detection = st.toggle("Object Detection", value=False)
        hand_tracing = st.toggle("Hand Tracing", value=False)
        
        viz_styles = []
        if object_detection:
            viz_styles = st.multiselect(
                "Viz Style",
                ["Bounding Box", "Label", "Filled Box", "Centroid", "Blur"],
                default=["Bounding Box", "Label"],
                label_visibility="collapsed"
            )
    with col_cam3:
        cameras = list_cameras()
        selected_camera = st.selectbox("Camera Source", cameras, index=0)

    # Initialize MediaPipe Hands (Cached)
    @st.cache_resource
    def get_hand_tracker():
        import mediapipe as mp
        mp_hands = mp.solutions.hands
        hands = mp_hands.Hands(
            static_image_mode=False,
            max_num_hands=2,
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5
        )
        return hands, mp.solutions.drawing_utils, mp_hands

    def draw_detections(frame, detections, styles):
        for det in detections:
            x1, y1, x2, y2 = map(int, det['box'])
            
            # Ensure coordinates are within frame bounds
            h, w, _ = frame.shape
            x1, y1 = max(0, x1), max(0, y1)
            x2, y2 = min(w, x2), min(h, y2)

            # Blur (Privacy)
            if "Blur" in styles:
                roi = frame[y1:y2, x1:x2]
                if roi.size > 0:
                    roi = cv2.GaussianBlur(roi, (51, 51), 0)
                    frame[y1:y2, x1:x2] = roi

            # Filled Box
            if "Filled Box" in styles:
                overlay = frame.copy()
                cv2.rectangle(overlay, (x1, y1), (x2, y2), (0, 120, 255), -1)
                alpha = 0.3
                cv2.addWeighted(overlay, alpha, frame, 1 - alpha, 0, frame)

            # Bounding Box
            if "Bounding Box" in styles:
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)

            # Centroid
            if "Centroid" in styles:
                cx, cy = (x1 + x2) // 2, (y1 + y2) // 2
                cv2.circle(frame, (cx, cy), 5, (0, 0, 255), -1)

            # Label
            if "Label" in styles:
                label = f"{det['label']} {det['score']}"
                cv2.putText(frame, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

    # Camera Feed
    if camera_power:
        if selected_camera == "Browser Camera":
            # Use Streamlit's native camera input for browser access
            img_file_buffer = st.camera_input("Live Feed (Browser)")
            if img_file_buffer is not None:
                # To read image file buffer with OpenCV:
                bytes_data = img_file_buffer.getvalue()
                cv2_img = cv2.imdecode(np.frombuffer(bytes_data, np.uint8), cv2.IMREAD_COLOR)
                
                if object_detection:
                    detections = detect_objects_in_frame(cv2_img)
                    draw_detections(cv2_img, detections, viz_styles)
                
                if hand_tracing:
                    hands, mp_drawing, mp_hands = get_hand_tracker()
                    # MediaPipe needs RGB
                    img_rgb = cv2.cvtColor(cv2_img, cv2.COLOR_BGR2RGB)
                    results = hands.process(img_rgb)
                    if results.multi_hand_landmarks:
                        for hand_landmarks in results.multi_hand_landmarks:
                            mp_drawing.draw_landmarks(
                                cv2_img, 
                                hand_landmarks, 
                                mp_hands.HAND_CONNECTIONS
                            )

                # Display processed frame
                frame_rgb = cv2.cvtColor(cv2_img, cv2.COLOR_BGR2RGB)
                st.image(frame_rgb, channels="RGB", use_column_width=True)

        else:
            # Backend/Simulated Camera
            frame = get_camera_frame(selected_camera)
            
            if object_detection:
                detections = detect_objects_in_frame(frame)
                draw_detections(frame, detections, viz_styles)

            if hand_tracing:
                hands, mp_drawing, mp_hands = get_hand_tracker()
                # MediaPipe needs RGB
                img_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                results = hands.process(img_rgb)
                if results.multi_hand_landmarks:
                    for hand_landmarks in results.multi_hand_landmarks:
                        mp_drawing.draw_landmarks(
                            frame, 
                            hand_landmarks, 
                            mp_hands.HAND_CONNECTIONS
                        )

            # Convert BGR to RGB for Streamlit
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            st.image(frame_rgb, caption=f"Live Feed: {selected_camera}", use_column_width=True)
    else:
        st.image("https://placehold.co/640x360/black/white?text=Camera+Feed+Offline", caption="Camera Feed (Offline)", use_column_width=True)
    
    # Audio Visualizer
    st.markdown("### Audio Spectrum")
    
    # Audio Controls
    col_audio1, col_audio2 = st.columns([1, 2])
    with col_audio1:
        audio_source = st.selectbox("Audio Source", ["Simulated", "Browser Microphone"], index=0)
    
    audio_data = None
    if audio_source == "Browser Microphone":
        audio_input = st.audio_input("Record Audio")
        if audio_input:
            audio_data = audio_input.getvalue()
    
    # Get visualizer data (real or simulated)
    chart_data = get_audio_visualizer_data(audio_data if audio_source == "Browser Microphone" else None)
    
    st.bar_chart(chart_data, height=150)
    
    # Controls
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Record Clip"):
            record_clip()
            st.success("Clip recorded!")
    with col2:
        if st.button("Mute Audio"):
            st.info("Audio muted.")

    # Monitoring Start/Stop Controls
    col3, col4 = st.columns(2)
    with col3:
        if st.button("Start Monitoring"):
            st.session_state.av_status = "Active"
            st.session_state.stop_av = False
            
    with col4:
        if st.button("Stop Monitoring"):
            st.session_state.av_status = "Idle"
            st.session_state.stop_av = True
            
    st.write(f"Feed status: {st.session_state.av_status}")
    
    if st.session_state.av_status == "Active":
        frame = get_camera_frame()
        if frame is not None:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            st.image(frame, channels="RGB", use_column_width=True)

        audio_bytes = get_audio_chunk()
        if audio_bytes:
            # Note: Frequent audio updates might cause stuttering in Streamlit
            st.audio(audio_bytes, format="audio/wav")

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
# Function: render_system_health_and_logs
# ----------------------------------------------------------------------
def render_system_health_and_logs():
    """
    Render the System Health & Logs panel with system metrics.
    """
    st.subheader("System Health")
    
    # System Metrics
    metrics = get_system_metrics()
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("CPU Usage", f"{metrics['cpu_percent']}%")
    with col2:
        st.metric("Memory Usage", f"{metrics['memory_percent']}%")
    with col3:
        st.metric("Disk Usage", f"{metrics['disk_percent']}%")
        
    st.markdown("---")
    st.markdown("### Recent Logs")
    
    logs = get_system_logs()
    if logs:
        for log in logs:
            st.text(f"[{log['timestamp']}] {log['message']}")
    else:
        st.info("No logs available.")
    
    if st.button("Trigger System Restart"):
        trigger_restart()
        st.success("Restart command sent!")
