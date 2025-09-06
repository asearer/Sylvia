"""
gui.py

GUI-based chat interface for Sylvia with live personality visualization,
weighted hybrid sliders, feedback buttons, and terminal logging.
"""

import sys
import io
import time
import tkinter as tk
from tkinter import messagebox, scrolledtext, StringVar, OptionMenu
from pathlib import Path
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Add Sylvia app root to sys.path if needed
sys.path.append(str(Path(__file__).parent.parent))

from src.bot.sylvia import SylviaBot
from personality.ai_personality.personality.visualizer_gui import PersonalityGUIVisualizer


class SylviaChatGUI:
    """GUI application for interacting with SylviaBot."""

    def __init__(self, master):
        """Initialize GUI, SylviaBot, and Personality visualization."""
        self.master = master
        master.title("Sylvia Chatbot")
        self.bot_name = "Sylvia"

        # Initialize bot
        self.bot = SylviaBot()
        self.persona = self.bot.personality
        self.visualizer = PersonalityGUIVisualizer(self.persona)

        # Last message tracking
        self.last_user_message = None
        self.last_bot_response = None

        # Terminal light/dark mode
        self.terminal_mode = "light"
        self.terminal_bg_light = "#f0f0f0"
        self.terminal_fg_light = "#000000"
        self.terminal_bg_dark = "#1e1e1e"
        self.terminal_fg_dark = "#f0f0f0"

        # ----------------------
        # Main horizontal pane: visualization | chat+terminal
        # ----------------------
        self.main_pane = tk.PanedWindow(master, orient=tk.HORIZONTAL)
        self.main_pane.pack(fill=tk.BOTH, expand=True)

        # Left pane: visualization
        self.viz_frame = tk.Frame(self.main_pane)
        self.main_pane.add(self.viz_frame, minsize=200)
        self.canvas = FigureCanvasTkAgg(self.visualizer.fig, master=self.viz_frame)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        self.canvas.draw()

        # Right pane: vertical chat + terminal (50/50)
        self.right_pane = tk.PanedWindow(self.main_pane, orient=tk.VERTICAL)
        self.main_pane.add(self.right_pane, minsize=300)

        # Chat panel (top)
        self.chat_frame = tk.Frame(self.right_pane)
        self.right_pane.add(self.chat_frame, minsize=200)
        self.chat_frame.pack_propagate(False)

        # Terminal panel (bottom)
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

        # ----------------------
        # Horizontal split inside chat panel: messages | input+controls
        # ----------------------
        self.chat_pane = tk.PanedWindow(self.chat_frame, orient=tk.HORIZONTAL)
        self.chat_pane.pack(fill=tk.BOTH, expand=True)

        # Chat messages (left)
        self.messages_frame = tk.Frame(self.chat_pane)
        self.chat_pane.add(self.messages_frame, minsize=500)
        self.chat_window = scrolledtext.ScrolledText(
            self.messages_frame, wrap=tk.WORD, state=tk.DISABLED
        )
        self.chat_window.pack(fill=tk.BOTH, expand=True)

        # Input + controls (right)
        self.input_control_frame = tk.Frame(self.chat_pane)
        self.chat_pane.add(self.input_control_frame, minsize=500)

        # ----------------------
        # Input frame
        # ----------------------
        input_frame = tk.Frame(self.input_control_frame)
        input_frame.pack(fill=tk.X, padx=5, pady=5)
        self.input_box = tk.Entry(input_frame)
        self.input_box.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5))
        self.input_box.bind("<Return>", self.send_message)
        self.send_btn = tk.Button(input_frame, text="Send", command=self.send_message)
        self.send_btn.pack(side=tk.LEFT)

        # ----------------------
        # Personality & hybrid controls
        # ----------------------
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

        # ----------------------
        # Feedback buttons
        # ----------------------
        feedback_frame = tk.Frame(self.input_control_frame)
        feedback_frame.pack(pady=5)
        self.positive_fb = tk.Button(feedback_frame, text="👍", command=lambda: self.send_feedback(1))
        self.positive_fb.pack(side=tk.LEFT, padx=5)
        self.negative_fb = tk.Button(feedback_frame, text="👎", command=lambda: self.send_feedback(-1))
        self.negative_fb.pack(side=tk.LEFT, padx=5)

        # Terminal mode toggle
        self.toggle_btn = tk.Button(self.input_control_frame, text="Toggle Terminal Mode", command=self.toggle_terminal_mode)
        self.toggle_btn.pack(pady=5)

        # Keyboard shortcuts
        master.bind("<Escape>", lambda e: master.quit())

        # Initial visualization update
        self.update_visualizer()

    # ----------------------
    # Terminal logging
    # ----------------------
    def log_terminal(self, message):
        """Thread-safe logging to terminal pane."""
        self.master.after(0, lambda: self.append_terminal(message))

    def append_chat(self, speaker, message):
        """Append message to chat pane."""
        self.chat_window.config(state=tk.NORMAL)
        self.chat_window.insert(tk.END, f"{speaker}: {message}\n")
        self.chat_window.config(state=tk.DISABLED)
        self.chat_window.see(tk.END)

    def append_terminal(self, message):
        """Append message to terminal pane."""
        self.terminal_window.config(state=tk.NORMAL)
        self.terminal_window.insert(tk.END, f"{message}\n")
        self.terminal_window.config(state=tk.DISABLED)
        self.terminal_window.see(tk.END)

    def toggle_terminal_mode(self):
        """Toggle terminal between light and dark mode."""
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
        """Handle user input and bot response."""
        user_msg = self.input_box.get().strip()
        if not user_msg:
            return
        self.append_chat("You", user_msg)
        self.log_terminal(f"Input: {user_msg}")
        self.input_box.delete(0, tk.END)

        start_time = time.time()

        old_stdout = sys.stdout
        sys.stdout = io.StringIO()
        try:
            bot_response = self.bot.get_response(user_msg)
            internal_output = sys.stdout.getvalue()
        finally:
            sys.stdout = old_stdout

        end_time = time.time()
        self.log_terminal(f"Processing time: {end_time - start_time:.3f}s")
        if internal_output.strip():
            self.log_terminal(f"Debug: {internal_output.strip()}")

        self.append_chat(self.bot_name, bot_response)
        self.log_terminal(f"Output: {bot_response}")

        self.last_user_message = user_msg
        self.last_bot_response = bot_response
        self.update_visualizer()

    def send_feedback(self, feedback_value):
        """Send feedback to Personality engine."""
        if self.last_user_message and self.last_bot_response:
            self.persona._automatic_evolution(self.last_user_message, self.last_bot_response, feedback_value)
            self.persona.save()
            self.update_visualizer()
            self.append_chat(self.bot_name, "Feedback recorded ✅")
            self.log_terminal(f"Feedback: {feedback_value}")
        else:
            messagebox.showinfo("Info", "Send a message before giving feedback.")

    # ----------------------
    # Personality dropdown
    # ----------------------
    def switch_personality_dropdown(self, value):
        """Switch active personality."""
        try:
            self.persona.switch_personality(value)
            self.update_visualizer()
            self.append_chat(self.bot_name, f"Switched to {value}")
            self.log_terminal(f"Personality switched to {value}")
        except ValueError as e:
            messagebox.showerror("Error", str(e))

    # ----------------------
    # Weighted hybrid sliders
    # ----------------------
    def dynamic_hybrid_dialog(self):
        """Weighted hybrid sliders popup dialog."""
        profiles = list(self.persona.profiles.keys())
        weight_sliders = {}

        dialog = tk.Toplevel(self.master)
        dialog.title("Assign Weights for Weighted Hybrid")
        tk.Label(dialog, text="Set weights (0–1) for each profile using sliders:").pack(pady=5)

        for profile in profiles:
            frame = tk.Frame(dialog)
            frame.pack(pady=2, fill=tk.X, padx=10)
            tk.Label(frame, text=profile, width=15, anchor='w').pack(side=tk.LEFT)
            slider = tk.Scale(frame, from_=0, to=1, resolution=0.01, orient=tk.HORIZONTAL, length=200)
            slider.pack(side=tk.LEFT)
            weight_sliders[profile] = slider

        def apply_weights():
            weights = {p: s.get() for p, s in weight_sliders.items() if s.get() > 0}
            if not weights:
                messagebox.showerror("Invalid Input", "At least one weight must be > 0")
                return
            try:
                self.persona.set_weighted_hybrid(weights)
                self.update_visualizer()
                self.append_chat(
                    self.bot_name,
                    f"Weighted hybrid active: {', '.join([f'{k}({v:.2f})' for k,v in weights.items()])}"
                )
                self.log_terminal(f"Weighted hybrid set: {weights}")
                dialog.destroy()
            except ValueError as e:
                messagebox.showerror("Error", str(e))

        tk.Button(dialog, text="Apply", command=apply_weights).pack(pady=10)

    # ----------------------
    # Visualization
    # ----------------------
    def update_visualizer(self):
        """Refresh personality visualization and hybrid weight bars."""
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
    app = SylviaChatGUI(root)
    root.mainloop()
