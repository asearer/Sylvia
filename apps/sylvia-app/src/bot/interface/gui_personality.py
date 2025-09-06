"""
gui_personality.py

GUI interface for Sylvia's Personality engine with:
- Live personality visualization
- Hybrid weight sliders
- Feedback buttons
- Terminal logging
"""

import sys
import os
import tkinter as tk
from tkinter import messagebox, scrolledtext, StringVar, OptionMenu
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from pathlib import Path
import time

# Add personality engine to path
sys.path.append(os.path.join(os.path.dirname(__file__), '../../libs/ai_personality'))

from personality.personality import Personality
from personality.visualizer_gui import PersonalityGUIVisualizer


class PersonalityChatApp:
    """GUI application for interacting with Sylvia's Personality engine."""

    def __init__(self, master):
        self.master = master
        master.title("Sylvia Chatbot")
        self.bot_name = "Sylvia"

        # Initialize engine and visualizer
        profiles_path = Path(__file__).parent / "personality" / "profiles.json"
        self.persona = Personality("astronaut", profiles_path=profiles_path, evolving=True)
        self.visualizer = PersonalityGUIVisualizer(self.persona)

        self.last_user_message = None
        self.last_bot_response = None

        # Session state for visualization
        self.session_state = {
            'weights_history': [],
            'micro_count_history': [],
            'interactions_history': []
        }

        # Terminal light/dark mode
        self.terminal_mode = "light"
        self.terminal_bg_light = "#f0f0f0"
        self.terminal_fg_light = "#000000"
        self.terminal_bg_dark = "#1e1e1e"
        self.terminal_fg_dark = "#f0f0f0"

        # --- Layout ---
        self._create_layout()
        self.update_visualizer()

    # ----------------------
    # Layout Setup
    # ----------------------
    def _create_layout(self):
        """Initialize GUI panes and widgets."""

        # Main horizontal pane: visualization | chat+terminal
        self.main_pane = tk.PanedWindow(self.master, orient=tk.HORIZONTAL)
        self.main_pane.pack(fill=tk.BOTH, expand=True)

        # Left: visualization
        self.viz_frame = tk.Frame(self.main_pane)
        self.main_pane.add(self.viz_frame, minsize=200)
        self.canvas = FigureCanvasTkAgg(self.visualizer.fig, master=self.viz_frame)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        self.canvas.draw()

        # Right: chat + terminal
        self.right_pane = tk.PanedWindow(self.main_pane, orient=tk.VERTICAL)
        self.main_pane.add(self.right_pane, minsize=300)

        # Chat frame
        self.chat_frame = tk.Frame(self.right_pane)
        self.right_pane.add(self.chat_frame, minsize=200)
        self.chat_frame.pack_propagate(False)

        # Terminal frame
        self.terminal_frame = tk.Frame(self.right_pane)
        self.right_pane.add(self.terminal_frame, minsize=200)
        self.terminal_frame.pack_propagate(False)
        self.terminal_window = scrolledtext.ScrolledText(
            self.terminal_frame,
            wrap=tk.WORD,
            state=tk.DISABLED,
            bg=self.terminal_bg_light,
            fg=self.terminal_fg_light
        )
        self.terminal_window.pack(fill=tk.BOTH, expand=True)

        # Chat horizontal split: messages | input + controls
        self.chat_pane = tk.PanedWindow(self.chat_frame, orient=tk.HORIZONTAL)
        self.chat_pane.pack(fill=tk.BOTH, expand=True)

        # Messages
        self.messages_frame = tk.Frame(self.chat_pane)
        self.chat_pane.add(self.messages_frame, minsize=500)
        self.chat_window = scrolledtext.ScrolledText(self.messages_frame, wrap=tk.WORD, state=tk.DISABLED)
        self.chat_window.pack(fill=tk.BOTH, expand=True)

        # Input & controls
        self.input_control_frame = tk.Frame(self.chat_pane)
        self.chat_pane.add(self.input_control_frame, minsize=500)
        self._create_input_controls()

        # Keyboard shortcut to quit
        self.master.bind("<Escape>", lambda e: self.master.quit())

    def _create_input_controls(self):
        """Input box, send button, personality/hybrid controls, feedback buttons."""
        # Input frame
        input_frame = tk.Frame(self.input_control_frame)
        input_frame.pack(fill=tk.X, padx=5, pady=5)
        self.input_box = tk.Entry(input_frame)
        self.input_box.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5))
        self.input_box.bind("<Return>", self.send_message)
        self.send_btn = tk.Button(input_frame, text="Send", command=self.send_message)
        self.send_btn.pack(side=tk.LEFT)

        # Personality & hybrid
        control_frame = tk.Frame(self.input_control_frame)
        control_frame.pack(pady=5)
        self.selected_personality = StringVar()
        self.selected_personality.set(list(self.persona.profiles.keys())[0])
        self.personality_menu = OptionMenu(
            control_frame,
            self.selected_personality,
            *self.persona.profiles.keys(),
            command=self.switch_personality_dropdown
        )
        self.personality_menu.pack(side=tk.LEFT, padx=5)
        self.hybrid_btn = tk.Button(control_frame, text="Set Weighted Hybrid", command=self.dynamic_hybrid_dialog)
        self.hybrid_btn.pack(side=tk.LEFT, padx=5)

        # Feedback buttons
        feedback_frame = tk.Frame(self.input_control_frame)
        feedback_frame.pack(pady=5)
        self.positive_fb = tk.Button(feedback_frame, text="👍", command=lambda: self.send_feedback(1))
        self.positive_fb.pack(side=tk.LEFT, padx=5)
        self.negative_fb = tk.Button(feedback_frame, text="👎", command=lambda: self.send_feedback(-1))
        self.negative_fb.pack(side=tk.LEFT, padx=5)

        # Terminal mode toggle
        self.toggle_btn = tk.Button(self.input_control_frame, text="Toggle Terminal Mode", command=self.toggle_terminal_mode)
        self.toggle_btn.pack(pady=5)

    # ----------------------
    # Terminal / logging
    # ----------------------
    def log_terminal(self, message):
        """Append message to terminal in thread-safe way."""
        self.master.after(0, lambda: self.append_terminal(message))

    def append_terminal(self, message):
        self.terminal_window.config(state=tk.NORMAL)
        self.terminal_window.insert(tk.END, f"{message}\n")
        self.terminal_window.config(state=tk.DISABLED)
        self.terminal_window.see(tk.END)

    def toggle_terminal_mode(self):
        if self.terminal_mode == "light":
            self.terminal_window.config(bg=self.terminal_bg_dark, fg=self.terminal_fg_dark)
            self.terminal_mode = "dark"
        else:
            self.terminal_window.config(bg=self.terminal_bg_light, fg=self.terminal_fg_light)
            self.terminal_mode = "light"

    # ----------------------
    # Chat handling
    # ----------------------
    def send_message(self, event=None):
        msg = self.input_box.get().strip()
        if not msg:
            return
        self.append_chat("You", msg)
        self.log_terminal(f"Input received: {msg}")
        self.input_box.delete(0, tk.END)

        start_time = time.time()
        old_stdout = sys.stdout
        sys.stdout = sys.__stdout__
        try:
            response = self.persona.chat(msg)
        finally:
            sys.stdout = old_stdout
        elapsed = time.time() - start_time

        self.log_terminal(f"Processing time: {elapsed:.3f}s")
        self.append_chat(self.bot_name, response)
        self.log_terminal(f"Output: {response}")

        self.last_user_message = msg
        self.last_bot_response = response
        self.update_visualizer()

    def append_chat(self, speaker, message):
        self.chat_window.config(state=tk.NORMAL)
        self.chat_window.insert(tk.END, f"{speaker}: {message}\n")
        self.chat_window.config(state=tk.DISABLED)
        self.chat_window.see(tk.END)

    def send_feedback(self, feedback_value):
        if self.last_user_message and self.last_bot_response:
            self.persona._automatic_evolution(
                self.last_user_message, self.last_bot_response, feedback_value
            )
            self.persona.save()
            self.update_visualizer()
            self.append_chat(self.bot_name, "Feedback recorded ✅")
            self.log_terminal(f"Feedback: {feedback_value}")
        else:
            messagebox.showinfo("Info", "Send a message before giving feedback.")

    # ----------------------
    # Personality / hybrid handling
    # ----------------------
    def switch_personality_dropdown(self, value):
        try:
            self.persona.switch_personality(value)
            self.update_visualizer()
            self.append_chat(self.bot_name, f"Switched to {value}")
            self.log_terminal(f"Personality switched to {value}")
        except ValueError as e:
            messagebox.showerror("Error", str(e))

    def dynamic_hybrid_dialog(self):
        profiles = list(self.persona.profiles.keys())
        sliders = {}
        dialog = tk.Toplevel(self.master)
        dialog.title("Assign Hybrid Weights")
        tk.Label(dialog, text="Set weights (0–1) for each profile:").pack(pady=5)
        for p in profiles:
            frame = tk.Frame(dialog)
            frame.pack(pady=2, fill=tk.X, padx=10)
            tk.Label(frame, text=p, width=15, anchor='w').pack(side=tk.LEFT)
            slider = tk.Scale(frame, from_=0, to=1, resolution=0.01, orient=tk.HORIZONTAL, length=200)
            slider.pack(side=tk.LEFT)
            sliders[p] = slider

        def apply_weights():
            weights = {p: s.get() for p, s in sliders.items() if s.get() > 0}
            if not weights:
                messagebox.showerror("Invalid Input", "At least one weight must be > 0")
                return
            self.persona.set_weighted_hybrid(weights)
            self.update_visualizer()
            self.append_chat(self.bot_name, f"Weighted hybrid: {', '.join([f'{k}({v:.2f})' for k,v in weights.items()])}")
            self.log_terminal(f"Weighted hybrid set: {weights}")
            dialog.destroy()

        tk.Button(dialog, text="Apply", command=apply_weights).pack(pady=10)

    # ----------------------
    # Visualization
    # ----------------------
    def update_visualizer(self):
        self.visualizer.update_history()
        weights = getattr(self.persona, "active_hybrid_weights", None)
        if weights:
            if not hasattr(self, "bar_ax"):
                self.bar_ax = self.visualizer.fig.add_axes([0.7, 0.05, 0.25, 0.25])
            self.bar_ax.clear()
            self.bar_ax.bar(weights.keys(), weights.values(), color='orange')
            self.bar_ax.set_title("Hybrid Weights")
            self.bar_ax.set_ylim(0, 1)
        elif hasattr(self, "bar_ax"):
            self.bar_ax.clear()
        self.canvas.draw()


if __name__ == "__main__":
    root = tk.Tk()
    app = PersonalityChatApp(root)
    root.mainloop()
