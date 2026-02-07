
import streamlit as st
import time
import json
import redis
import threading
import os
import sys

# Import script context helper
from streamlit.runtime.scriptrunner import add_script_run_ctx

# Add project root to path
sys.path.append("/app")

# Try to import Messenger, fallback to direct redis if libs not found (local run vs docker)
try:
    from libs.ipc.messenger import Messenger
except ImportError:
    # Fallback for local run without installing libs package
    class Messenger:
        def __init__(self, channel="sylvia:events"):
            self.redis = redis.Redis(host=os.getenv("REDIS_HOST", "localhost"), port=6379, decode_responses=True)
            self.channel = channel
            self.pubsub = self.redis.pubsub()

        def publish(self, event_type, payload):
            msg = json.dumps({"type": event_type, "payload": payload})
            self.redis.publish(self.channel, msg)

        def subscribe(self, handler):
            self.pubsub.subscribe(self.channel)
            for message in self.pubsub.listen():
                if message["type"] == "message":
                    try:
                        data = json.loads(message["data"])
                        handler(data.get("type"), data.get("payload"))
                    except:
                        pass
        
        def close(self):
            self.pubsub.close()
            self.redis.close()

# Page Config
st.set_page_config(page_title="Sylvia Dashboard", layout="wide")

# Styling
st.markdown("""
<style>
    .stTextInput > div > div > input {
        background-color: #2b2b2b;
        color: white;
    }
    .chat-msg {
        padding: 10px;
        border-radius: 5px;
        margin-bottom: 5px;
    }
    .user-msg {
        background-color: #0e639c;
        color: white;
        text-align: right;
    }
    .agent-msg {
        background-color: #333333;
        color: #e0e0e0;
    }
</style>
""", unsafe_allow_html=True)

# Session State
if "messages" not in st.session_state:
    st.session_state.messages = []

# Initialize Messenger
if "messenger" not in st.session_state:
    try:
        st.session_state.messenger = Messenger(channel="sylvia:events")
    except Exception as e:
        st.error(f"Failed to connect to Redis: {e}")
        st.session_state.messenger = None

# Background Listener
def listener_thread():
    # We must access session state carefully.
    # With add_script_run_ctx, we should be able to access it.
    if "messenger" not in st.session_state or not st.session_state.messenger:
        return
        
    def handler(event_type, payload):
        try:
            if event_type == "agent_response":
                st.session_state.messages.append({"role": "agent", "content": payload})
                # Rerun to update UI
                st.rerun()
            elif event_type == "user_input": # Echo from STT
                st.session_state.messages.append({"role": "user", "content": f"(Voice) {payload}"})
                st.rerun()
        except Exception as e:
            print(f"Error in handler: {e}")

    try:
        st.session_state.messenger.subscribe(handler)
    except Exception as e:
        print(f"Listener error: {e}")

if "listener_started" not in st.session_state:
    if st.session_state.messenger:
        t = threading.Thread(target=listener_thread, daemon=True)
        # Attach the current script context to the thread
        add_script_run_ctx(t)
        t.start()
        st.session_state.listener_started = True

# UI Layout
st.title("Sylvia Interaction Dashboard")

col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("Chat")
    
    # Display Chat
    for msg in st.session_state.messages:
        role_class = "user-msg" if msg["role"] == "user" else "agent-msg"
        st.markdown(f"<div class='chat-msg {role_class}'>{msg['content']}</div>", unsafe_allow_html=True)

    # Input
    with st.form("chat_form", clear_on_submit=True):
        user_input = st.text_input("Message")
        submitted = st.form_submit_button("Send")
        
        if submitted and user_input and st.session_state.messenger:
            # Publish to backend
            st.session_state.messages.append({"role": "user", "content": user_input})
            st.session_state.messenger.publish("user_input", user_input)
            st.rerun()

with col2:
    st.subheader("Status")
    if st.session_state.messenger:
        st.success("Connected to Event Bus")
    else:
        st.error("Disconnected (Redis unavailable)")
        
    st.markdown("### Active Services")
    st.markdown("- **Agent Core**: ✅ Online")
    st.markdown("- **Voice STT**: ✅ Online")
    st.markdown("- **Voice TTS**: ✅ Online")
    st.markdown("- **Avatar Bridge**: ✅ Online")

    st.markdown("### Avatar")
    
    # Allow manual override of the WebSocket URL (useful for remote setups)
    default_ws = "ws://localhost:8765"
    if "ws_url" not in st.session_state:
        st.session_state.ws_url = default_ws
        
    # We use a text input that updates an iframe query param or is injected
    # Since we can't easily inject into the iframe dynamically without rerun, we use the value in the HTML template.
    
    col_av1, col_av2 = st.columns([3, 1])
    with col_av1:
        st.info("Avatar rendering enabled.")
    with col_av2:
        # Toggle for settings
        show_settings = st.toggle("Settings", value=False)
        
    if show_settings:
        st.session_state.ws_url = st.text_input("Bridge URL", value=st.session_state.ws_url)

    # Three.js Avatar Client with injected URL
    # NOTE: We use a standard string and .replace() to avoid f-string syntax errors with JS/CSS braces
    html_template = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <style>
            body { margin: 0; overflow: hidden; background-color: #0e1117; }
            #avatar-container { width: 100%; height: 300px; }
            #status { position: absolute; top: 10px; left: 10px; color: lime; font-family: monospace; font-size: 10px; }
        </style>
        <script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
    </head>
    <body>
        <div id="status">Connecting...</div>
        <div id="avatar-container"></div>
        <script>
            const TARGET_WS_URL = "__WS_URL__";
            // Scene Setup
            const container = document.getElementById('avatar-container');
            const scene = new THREE.Scene();
            scene.background = new THREE.Color(0x0e1117); // Match Streamlit dark theme

            const camera = new THREE.PerspectiveCamera(50, container.clientWidth / container.clientHeight, 0.1, 1000);
            camera.position.z = 5;

            const renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true });
            renderer.setSize(container.clientWidth, container.clientHeight);
            container.appendChild(renderer.domElement);

            // Lighting
            const ambientLight = new THREE.AmbientLight(0xffffff, 0.5);
            scene.add(ambientLight);
            const directionalLight = new THREE.DirectionalLight(0xffffff, 1);
            directionalLight.position.set(2, 2, 5);
            scene.add(directionalLight);

            // Avatar Group
            const avatarGroup = new THREE.Group();
            scene.add(avatarGroup);

            // Head (Sphere)
            const headGeo = new THREE.SphereGeometry(1.2, 32, 32);
            const headMat = new THREE.MeshStandardMaterial({ color: 0x007acc, roughness: 0.3, metalness: 0.8 });
            const head = new THREE.Mesh(headGeo, headMat);
            avatarGroup.add(head);

            // Eyes
            const eyeGeo = new THREE.SphereGeometry(0.3, 16, 16);
            const eyeMat = new THREE.MeshStandardMaterial({ color: 0x000000, emissive: 0x00ff00, emissiveIntensity: 0.5 });
            
            const leftEye = new THREE.Mesh(eyeGeo, eyeMat);
            leftEye.position.set(-0.5, 0.3, 1.0);
            avatarGroup.add(leftEye);

            const rightEye = new THREE.Mesh(eyeGeo, eyeMat);
            rightEye.position.set(0.5, 0.3, 1.0);
            avatarGroup.add(rightEye);

            // Mouth (Capsule-like using Cylinder with rounded ends usually, or just a scaled sphere/box)
            const mouthGeo = new THREE.BoxGeometry(0.6, 0.1, 0.1);
            const mouthMat = new THREE.MeshStandardMaterial({ color: 0x000000 });
            const mouth = new THREE.Mesh(mouthGeo, mouthMat);
            mouth.position.set(0, -0.4, 1.1);
            avatarGroup.add(mouth);

            // Animation State
            let isSpeaking = false;
            let isListening = false;
            let time = 0;

            // WebSocket Connection
            const statusDiv = document.getElementById('status');
            let socket = null;

            function connect(url) {
                if (socket) {
                    socket.close();
                }
                statusDiv.textContent = "Attempting connect to: " + url;
                statusDiv.style.color = "yellow";
                
                try {
                    socket = new WebSocket(url);

                    socket.onopen = function() {
                        statusDiv.textContent = "SYS: ONLINE (" + url + ")";
                        statusDiv.style.color = "#00ff00";
                    };

                    socket.onmessage = function(event) {
                        try {
                            const msg = JSON.parse(event.data);
                            if (msg.type === "agent_response") {
                                isSpeaking = true;
                                isListening = false;
                                setTimeout(() => { isSpeaking = false; }, 3000);
                                head.material.color.setHex(0x007acc);
                                leftEye.material.emissive.setHex(0x00ff00);
                            } else if (msg.type === "user_input") {
                                isSpeaking = false;
                                isListening = true;
                                head.material.color.setHex(0xffaa00);
                                leftEye.material.emissive.setHex(0xff0000);
                                rightEye.material.emissive.setHex(0xff0000);
                            }
                        } catch (e) {}
                    };

                    socket.onerror = function(error) {
                        statusDiv.textContent = "ERR: Failed (" + url + ")";
                        statusDiv.style.color = "orange";
                    };

                    socket.onclose = function(event) {
                        if (!event.wasClean) {
                            statusDiv.textContent = "ERR: Closed (" + url + "). Check Port/Network.";
                            statusDiv.style.color = "red";
                        }
                    };
                } catch (e) {
                     statusDiv.textContent = "ERR: Invalid URL";
                }
            }

            // Initial Connect using injected Python variable
            connect(TARGET_WS_URL);

            // Animation Loop
            function animate() {
                requestAnimationFrame(animate);
                time += 0.05;

                // Idle Float
                avatarGroup.position.y = Math.sin(time) * 0.1;
                avatarGroup.rotation.y = Math.sin(time * 0.5) * 0.1;

                // Speaking Animation (Mouth scaling)
                if (isSpeaking) {
                    mouth.scale.y = 1 + Math.sin(time * 10) * 2;
                    mouth.scale.x = 0.8 + Math.cos(time * 10) * 0.2;
                } else {
                    mouth.scale.set(1, 1, 1);
                }

                // Breathing/Listening Pulse
                if (isListening) {
                   head.scale.setScalar(1 + Math.sin(time * 2) * 0.02); 
                } else {
                   head.scale.setScalar(1);
                }

                renderer.render(scene, camera);
            }

            animate();

            // Handle Resize
            window.addEventListener('resize', () => {
                camera.aspect = container.clientWidth / container.clientHeight;
                camera.updateProjectionMatrix();
                renderer.setSize(container.clientWidth, container.clientHeight);
            });
        </script>
    </body>
    </html>
    """
    
    import streamlit.components.v1 as components
    # Inject the actual URL
    clean_url = st.session_state.ws_url.strip()
    # Simple injection
    html_code = html_template.replace("__WS_URL__", clean_url)
    
    components.html(html_code, height=310)

    st.markdown("### Controls")
    if st.button("Clear History"):
        st.session_state.messages = []
        st.rerun()
