"""
Streamlit dashboard for interactive AI personality experimentation.
Includes live profile weights and micro-personality plots.
"""

import streamlit as st
import pandas as pd
import plotly.express as px
from ai_personality.personality import Personality

# Initialize personality
persona = Personality("astronaut", evolving=True)

# Initialize session state
if "weights_history" not in st.session_state:
    st.session_state.weights_history = []
if "micro_count_history" not in st.session_state:
    st.session_state.micro_count_history = []
if "interactions_history" not in st.session_state:
    st.session_state.interactions_history = []

st.set_page_config(page_title="AI personality Dashboard", layout="wide")
st.title("AI personality Interactive Dashboard with Live Plots")

# Sidebar for hybrid weight sliders
st.sidebar.header("Hybrid personality Weights")
profiles = list(persona.profiles.keys())
weights = {}
for profile in profiles:
    weights[profile] = st.sidebar.slider(
        f"{profile} weight", 0.0, 1.0, float(persona.active_profiles.get(profile, 0.0)), 0.05
    )

if st.sidebar.button("Apply Hybrid Weights"):
    total = sum(weights.values())
    if total == 0:
        st.sidebar.warning("Total weight cannot be zero")
    else:
        normalized_weights = {k: v/total for k, v in weights.items() if v > 0.0}
        persona.set_weighted_hybrid(normalized_weights)
        st.sidebar.success("Hybrid weights applied")

# Chat interface
st.subheader("Chat with AI")
user_input = st.text_input("Your message:")

if st.button("Send") and user_input.strip() != "":
    response = persona.chat(user_input)
    st.text_area("AI Response", value=response, height=150, max_chars=None, key=f"response_{persona.interactions}")

    # Feedback buttons
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Positive Feedback"):
            persona._automatic_evolution(user_input, response, feedback=1)
    with col2:
        if st.button("Negative Feedback"):
            persona._automatic_evolution(user_input, response, feedback=-1)

    persona.save()

    # Update history for plots
    st.session_state.interactions_history.append(persona.interactions)
    snapshot = persona.active_profiles.copy()
    for p in profiles:
        if p not in snapshot:
            snapshot[p] = 0.0
    st.session_state.weights_history.append(snapshot)
    micro_count = sum(1 for mp in persona.micro_personalities.values() if mp["weight"] > 0.05)
    st.session_state.micro_count_history.append(micro_count)

# Active profiles table
st.subheader("Active Profiles & Weights")
df_weights = pd.DataFrame({
    "Profile": list(persona.active_profiles.keys()),
    "Weight": list(persona.active_profiles.values())
})
st.dataframe(df_weights)

# Micro-personalities table
st.subheader("Emergent Micro-Personalities")
micro_data = []
for name, data in persona.micro_personalities.items():
    if data["weight"] > 0.05:
        quirks = ", ".join(data["quirks"] + data["idioms"])
        micro_data.append({"Name": name, "Weight": data["weight"], "Quirks/Idioms": quirks[:100]})
st.dataframe(pd.DataFrame(micro_data))

# Interaction statistics
st.subheader("Interaction Stats")
st.write(f"Total Interactions: {persona.interactions}")
st.write(f"Total Micro-Personalities: {len([mp for mp in persona.micro_personalities.values() if mp['weight']>0.05])}")
st.write(f"Total Words Tracked: {len(persona.history_words)}")

# Live profile weights plot
if st.session_state.interactions_history:
    st.subheader("Profile Weights Over Time")
    weight_records = []
    for i, snapshot in enumerate(st.session_state.weights_history):
        for profile, w in snapshot.items():
            weight_records.append({"Interaction": st.session_state.interactions_history[i],
                                   "Profile": profile, "Weight": w})
    df_plot = pd.DataFrame(weight_records)
    fig_weights = px.line(df_plot, x="Interaction", y="Weight", color="Profile",
                          markers=True, title="Profile Weights Evolution")
    st.plotly_chart(fig_weights, use_container_width=True)

    # Micro-personality count plot
    st.subheader("Micro-Personalities Count Over Time")
    df_micro = pd.DataFrame({
        "Interaction": st.session_state.interactions_history,
        "Micro-Personalities": st.session_state.micro_count_history
    })
    fig_micro = px.line(df_micro, x="Interaction", y="Micro-Personalities",
                        markers=True, title="Emergent Micro-Personalities Over Time")
    st.plotly_chart(fig_micro, use_container_width=True)
