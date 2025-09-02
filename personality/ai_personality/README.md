# **AI Personality Project**

## **Overview**

The **AI Personality Project** is an experimental framework for building adaptive AI chatbots with **customizable personalities**. It features:

* **Weighted hybrid personalities** – combine multiple personality profiles dynamically.
* **Emergent micro-personalities** – traits, quirks, and idioms evolve from interactions.
* **Automatic personality evolution** – adjusts tone, style, and behavior based on feedback and conversation.
* **Multiple interfaces**:

  * Console-based chat
  * GUI chat with live Matplotlib plots
  * Streamlit web dashboard with live plots and interactive controls

This project is designed for experimentation, research, or as a foundation for advanced conversational AI systems.

---

## **Features**

* **Personality Profiles**: Easily define new profiles in `ai_personality/profiles.json` with attributes like tone, quirks, values, and greeting.
* **Weighted Hybrid**: Blend multiple profiles in real-time using weighted sliders or commands.
* **Micro-Personalities**: Automatically generate emergent traits from repeated words and patterns.
* **Automatic Evolution**: Personality traits adjust based on user feedback, sentiment, and interactions.
* **Style Rewriting**: AI responses are rewritten to reflect the active personality’s tone and quirks.
* **Visualization**:

  * Console: Active profiles, micro-personalities, and stats
  * GUI: Live plots of profile weights and micro-personality counts
  * Streamlit: Interactive sliders, chat, and live plots

---

## **Project Structure**

```
ai_personality_project/
├── ai_personality/             # Core package
│   ├── __init__.py
│   ├── personality.py          # Personality engine with evolution
│   ├── memory.py               # Conversation memory
│   ├── style_rewriter.py       # Response style rewriting
│   ├── visualizer.py           # Console visualization
│   ├── visualizer_gui.py       # Matplotlib GUI visualizer
│   └── profiles.json           # Default personality profiles
├── main.py                     # Console-based chat interface
├── main_gui.py                 # GUI chat interface with live plots
└── dashboard.py                # Streamlit web dashboard with live plots
```

---

## **Installation & Requirements**

1. Install Python 3.9+
2. Install required packages:

```bash
pip install langchain openai textblob streamlit plotly rich matplotlib
```

3. Make sure you have an **OpenAI API key** if using LangChain with OpenAI models. Set it as an environment variable:

```bash
export OPENAI_API_KEY="your_api_key_here"
```

---

## **Usage**

### **1. Console Chat**

```bash
python main.py
```

**Commands**:

* `/switch [profile]` – switch to a different personality profile
* `/hybrid [profile:weight,...]` – set weighted hybrid personalities
* `+` / `-` – provide feedback to influence evolution
* `quit` – exit the chat

---

### **2. GUI Chat with Live Plots**

```bash
python main_gui.py
```

* Graphical visualization shows **profile weights** and **micro-personality evolution** in real-time.
* Interactive feedback and hybrid profile adjustments are fully supported.

---

### **3. Streamlit Dashboard**

```bash
streamlit run dashboard.py
```

* Web-based interactive chat with sliders for hybrid weights.
* Live plots display **profile weights** and **micro-personality counts** over time.
* Provides buttons for positive/negative feedback.

---

## **Creating New Profiles**

1. Open `ai_personality/profiles.json`.
2. Add a new JSON object with keys:

```json
{
  "name": {
    "tone": "description of tone",
    "quirks": "list of quirks",
    "values": "core values",
    "knowledge_focus": "area of expertise",
    "interaction_style": "formal/informal style",
    "greeting": "opening message"
  }
}
```

3. Save the JSON and restart any interface.

---

## **Advanced Features**

* **Automatic Evolution**: Personality adapts over time to user interactions and feedback.
* **Micro-Personalities**: Track emergent traits for subtle conversational changes.
* **Weighted Hybrid Personalities**: Blend multiple profiles for dynamic personality combinations.

