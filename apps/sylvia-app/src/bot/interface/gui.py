# src/interface/gui.py

import tkinter as tk
from tkinter import scrolledtext, StringVar, OptionMenu
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from ai_personality.personality import Personality
from personality.ai_personality.personality.visualizer_gui import PersonalityGUIVisualizer
from libs.personality_helpers import snapshot_active_profiles, micro_personality_count, update_session_history

class SylviaGUI:
    def __init__(self, master):
        self.master = master
        master.title("Sylvia Chatbot")
        
        # Initialize bot personality
        self.bot_persona = Personality("astronaut", evolving=True)
        self.visualizer = PersonalityGUIVisualizer(self.bot_persona)

        # Session state for tracking history
        self.session_state = {
            'weights_history': [],
            'micro_count_history': [],
            'interactions_history': []
        }

        # Setup GUI panes
        self.setup_panes()

        # Update visualization
        self.update_visualizer()

    def setup_panes(self):
        # Chat display
        self.chat_display = scrolledtext.ScrolledText(self.master, state='disabled', width=60, height=20)
        self.chat_display.grid(row=0, column=0, columnspan=2, padx=10, pady=10)

        # User input
        self.user_input = StringVar()
        self.input_entry = tk.Entry(self.master, textvariable=self.user_input, width=50)
        self.input_entry.grid(row=1, column=0, padx=10, pady=5, sticky='ew')
        self.input_entry.focus_set()
        self.input_entry.bind('<Return>', self.send_message)

        self.send_btn = tk.Button(self.master, text="Send", command=self.send_message)
        self.send_btn.grid(row=1, column=1, padx=5, pady=5)

        # Personality dropdown
        self.selected_personality = StringVar()
        self.selected_personality.set(list(self.bot_persona.profiles.keys())[0])
        self.personality_menu = OptionMenu(
            self.master,
            self.selected_personality,
            *self.bot_persona.profiles.keys(),
            command=self.switch_personality_dropdown
        )
        self.personality_menu.grid(row=2, column=0, padx=10, pady=5)

        # Visualization canvas
        self.canvas = FigureCanvasTkAgg(self.visualizer.fig, master=self.master)
        self.canvas.get_tk_widget().grid(row=0, column=2, rowspan=3, padx=10, pady=10)

    def handle_user_input(self, msg):
        """
        Central function to handle all commands and normal chat input.
        """
        msg_lower = msg.lower()
        if msg_lower.startswith("/switch"):
            parts = msg.split()
            if len(parts) > 1:
                self.bot_persona.switch_personality(parts[1])
                update_session_history(self.bot_persona, self.session_state)
                self.update_visualizer()
                return f"Switched to {parts[1]}"

        if msg_lower.startswith("/hybrid"):
            parts = msg.split()
            if len(parts) > 1:
                weights = {}
                for pair in parts[1].split(","):
                    try:
                        name, w = pair.split(":")
                        weights[name] = float(w)
                    except:
                        return f"Invalid format: {pair}. Use Name:Weight"
                self.bot_persona.set_weighted_hybrid(weights)
                update_session_history(self.bot_persona, self.session_state)
                self.update_visualizer()
                return f"Weighted hybrid applied: {weights}"

        # Normal chat
        response = self.bot_persona.chat(msg)
        update_session_history(self.bot_persona, self.session_state)
        self.update_visualizer()
        return response

    def send_message(self, event=None):
        msg = self.user_input.get().strip()
        if not msg:
            return
        self.chat_display.config(state='normal')
        self.chat_display.insert(tk.END, f"You: {msg}\n")
        self.chat_display.config(state='disabled')
        self.chat_display.see(tk.END)
        self.user_input.set("")
        response = self.handle_user_input(msg)
        self.chat_display.config(state='normal')
        self.chat_display.insert(tk.END, f"Sylvia: {response}\n")
        self.chat_display.config(state='disabled')
        self.chat_display.see(tk.END)

    def switch_personality_dropdown(self, profile):
        self.bot_persona.switch_personality(profile)
        update_session_history(self.bot_persona, self.session_state)
        self.update_visualizer()

    def update_visualizer(self):
        self.visualizer.update_history()
        self.canvas.draw()

