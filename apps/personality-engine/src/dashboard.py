"""
dashboard.py

Streamlit dashboard for interactive AI personality experimentation.
Includes live profile weights and micro-personality plots.

Refactored for maintainability and session tracking.
"""

from typing import Dict, Optional
import streamlit as st
import pandas as pd
import plotly.express as px
from ai_personality.personality import Personality

# -------------------------
# Helper functions
# -------------------------
def normalize_weights(weights: Dict[str, float]) -> Dict[str, float]:
    """Normalize weights to sum to 1 and remove zeros."""
    total = sum(weights.values())
    if total == 0:
        return {}
    return {k: v / total for k, v in weights.items() if v > 0.0}


def snapshot_active_profiles(persona: Personality) -> Dict[str, float]:
    """Return a snapshot of all active profiles, including zero weights."""
    snapshot = persona.active_profiles.copy()
    for p in persona.profiles.keys():
        if p not in snapshot:
            snapshot[p] = 0.0
    return snapshot


def micro_personality_count(persona: Personality, threshold: float = 0.05) -> int:
    """Count micro-personalities with weight above threshold."""
    return sum(1 for mp in persona.micro_personalities.values() if mp["weight"] > threshold)


def update_session_history(persona: Personality):
    """Update Streamlit session history for plotting."""
    st.session_state.interactions_history.append(persona.interactions)
    st.session_state.weights_history.append(snapshot_active_profiles(persona))
    st.session_state.micro_count_history.append(micro_personality_count(persona))


def plot_weights_over_time() -> None:
    """Generate Plotly line chart for profile weights."""
    weight_records = []
    for i, snapshot in enumerate(st.session_state.weights_history):
        for profile, w in snapshot.items():
            weight_records.append({
                "Interaction": st.session_state.interactions_history[i],
                "Profile": profile,
                "Weight": w
            })
    df_plot = pd.DataFrame(weight_records)
    fig = px.line(df_plot, x="Interaction", y="Weight", color="Profile",
                  markers=True, title="Profile Weights Evolution")
    st.plotly_chart(fig, use_container_width=True)


def plot_micro_count_over_time() -> None:
    """Generate Plotly line chart for micro-personality count over time."""
    df_micro = pd.DataFrame({
        "Interaction": st.session_state.interactions_history,
        "Micro-Personalities": st.session_state.micro_count_history
    })
    fig = px.line(df_micro, x="Interaction", y="Micro-Personalities",
                  markers=True, title="Emergent Micro-Personalities Over Time")
    st.plotly_chart(fig, use_container_width=True)


# -------------------------
# Initialize Personality
# -------------------------
persona = Personality("astronaut", evolving=True)

# Initialize session state if not present
for key in ["weights_history", "micro_count_history", "interactions_history"]:
    if key not in st.session_state:
        st.session_state[key] = []

st.set_page_config(page_title="AI Personality Dashboard", layout="wide")
st.title("AI Personality Interactive Dashboard")

# -------------------------
# Sidebar: Hybrid Weights
# -------------------------
st.sidebar.header("Hybrid Personality Weights")
profiles = list(persona.profiles.keys())
weights = {}
for profile in profiles:
    weights[profile] = st.sidebar.slider(
        f"{profile} weight",
        min_value=0.0,
        max_value=1.0,
        value=float(persona.active_profiles.get(profile, 0.0)),
        step=0.05
    )

if st.sidebar.button("Apply Hybrid Weights"):
    normalized = normalize_weights(weights)
    if not normalized:
        st.sidebar.warning("Total weight cannot be zero")
    else:
        persona.set_weighted_hybrid(normalized)
        st.sidebar.success("Hybrid weights applied")
        update_session_history(persona)

if st.sidebar.button("Reset Session"):
    """Reset session history and persona state."""
    st.session_state.weights_history.clear()
    st.session_state.micro_count_history.clear()
    st.session_state.interactions_history.clear()
    persona.reset()  # Assuming the Personality class has a reset method
    st.sidebar.success("Session reset")


# -------------------------
# Chat Interface
# -------------------------
st.subheader("Chat with AI")
user_input = st.text_input("Your message:")

if st.button("Send") and user_input.strip() != "":
    response = persona.chat(user_input)
    st.text_area("AI Response", value=response, height=150, max_chars=None,
                 key=f"response_{persona.interactions}")

    # Feedback buttons
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Positive Feedback"):
            persona._automatic_evolution(user_input, response, feedback=1)
    with col2:
        if st.button("Negative Feedback"):
            persona._automatic_evolution(user_input, response, feedback=-1)

    persona.save()
    update_session_history(persona)

# -------------------------
# Tables
# -------------------------
st.subheader("Active Profiles & Weights")
df_weights = pd.DataFrame({
    "Profile": list(persona.active_profiles.keys()),
    "Weight": list(persona.active_profiles.values())
})
st.dataframe(df_weights)

st.subheader("Emergent Micro-Personalities")
micro_data = [
    {
        "Name": name,
        "Weight": data["weight"],
        "Quirks/Idioms": ", ".join(data["quirks"] + data["idioms"])[:100]
    }
    for name, data in persona.micro_personalities.items() if data["weight"] > 0.05
]
st.dataframe(pd.DataFrame(micro_data))

# -------------------------
# Plots
# -------------------------
if st.session_state.interactions_history:
    st.subheader("Profile Weights Over Time")
    plot_weights_over_time()

    st.subheader("Micro-Personalities Count Over Time")
    plot_micro_count_over_time()
