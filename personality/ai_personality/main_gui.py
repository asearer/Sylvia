"""
main_gui.py

Fully GUI-only chat interface with live plots using PersonalityGUIVisualizer.
Features:
- Horizontal resizable panels: personality visualization (left) and chat interface (right).
- Vertical resizable panels inside chat: chat history vs input + controls.
- Dropdown menu to switch personalities.
- Dynamic weighted hybrid creation via GUI using sliders for weights.
- Feedback buttons for user-driven evolution.
- Silenced internal debug prints from Personality engine.
- Keyboard shortcuts: Enter to send messages, Esc to quit.
- Bot consistently named "Sylvia" in chat.
"""

import sys
import os
import tkinter as tk
from tkinter import messagebox, scrolledtext, StringVar, OptionMenu
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import io
from pathlib import Path

# Add ai_personality folder to sys.path
sys.path.append(os.path.join(os.path.dirname(__file__)))

from personality.personality import Personality
from personality.visualizer_gui import PersonalityGUIVisualizer


class PersonalityChatApp:
    """
    GUI application for interacting with the Sylvia chatbot with live personality visualization.
    """

    def __init__(self, master):
        """
        Initialize the GUI, personality engine, and visualizer.

        Args:
            master (tk.Tk): The root Tkinter window.
        """
        self.master = master
        master.title("Sylvia Chatbot")

        # Bot name
        self.bot_name = "Sylvia"

        # Locate profiles.json relative to this file
        profiles_path = Path(__file__).parent / "personality" / "profiles.json"

        # Initialize Personality engine
        self.persona = Personality("astronaut", profiles_path=profiles_path, evolving=True)

        # Initialize visualizer for personality plots
        self.visualizer = PersonalityGUIVisualizer(self.persona)

        # Track last message for feedback
        self.last_user_message = None
        self.last_bot_response = None

        # --- Horizontal PanedWindow for visualization and chat ---
        self.main_pane = tk.PanedWindow(master, orient=tk.HORIZONTAL)
        self.main_pane.pack(fill=tk.BOTH, expand=True)

        # Left frame: Visualization
        self.viz_frame = tk.Frame(self.main_pane)
        self.main_pane.add(self.viz_frame, minsize=200)

        self.canvas = FigureCanvasTkAgg(self.visualizer.fig, master=self.viz_frame)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        self.canvas.draw()

        # Right frame: Chat (with vertical resizable panes)
        self.chat_pane = tk.PanedWindow(self.main_pane, orient=tk.VERTICAL)
        self.main_pane.add(self.chat_pane, minsize=300)

        # Top frame: Chat messages
        self.chat_frame = tk.Frame(self.chat_pane)
        self.chat_pane.add(self.chat_frame, minsize=200)

        self.chat_window = scrolledtext.ScrolledText(
            self.chat_frame, wrap=tk.WORD, state=tk.DISABLED
        )
        self.chat_window.pack(fill=tk.BOTH, expand=True)

        # Bottom frame: Input + controls
        self.input_control_frame = tk.Frame(self.chat_pane)
        self.chat_pane.add(self.input_control_frame, minsize=150)

        # --- Input frame ---
        input_frame = tk.Frame(self.input_control_frame)
        input_frame.pack(fill=tk.X, padx=5, pady=5)

        self.input_box = tk.Entry(input_frame)
        self.input_box.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5))
        self.input_box.bind("<Return>", self.send_message)

        self.send_btn = tk.Button(input_frame, text="Send", command=self.send_message)
        self.send_btn.pack(side=tk.LEFT)

        # --- Control frame for personality and hybrid dropdowns ---
        control_frame = tk.Frame(self.input_control_frame)
        control_frame.pack(pady=5)

        # Personality dropdown
        self.selected_personality = StringVar()
        self.selected_personality.set(list(self.persona.profiles.keys())[0])
        self.personality_menu = OptionMenu(
            control_frame,
            self.selected_personality,
            *self.persona.profiles.keys(),
            command=self.switch_personality_dropdown
        )
        self.personality_menu.pack(side=tk.LEFT, padx=5)

        # Weighted hybrid button
        self.hybrid_btn = tk.Button(control_frame, text="Set Weighted Hybrid", command=self.dynamic_hybrid_dialog)
        self.hybrid_btn.pack(side=tk.LEFT, padx=5)

        # Feedback buttons
        feedback_frame = tk.Frame(self.input_control_frame)
        feedback_frame.pack(pady=5)

        self.positive_fb = tk.Button(feedback_frame, text="👍", command=lambda: self.send_feedback(1))
        self.positive_fb.pack(side=tk.LEFT, padx=5)

        self.negative_fb = tk.Button(feedback_frame, text="👎", command=lambda: self.send_feedback(-1))
        self.negative_fb.pack(side=tk.LEFT, padx=5)

        # Keyboard shortcut to quit
        master.bind("<Escape>", lambda e: master.quit())

        # Initial visualization update
        self.update_visualizer()

    # ----------------------
    # Chat methods
    # ----------------------
    def append_chat(self, speaker, message):
        """
        Append a message to the chat window.

        Args:
            speaker (str): Speaker name (e.g., "You", "Sylvia").
            message (str): Message content.
        """
        self.chat_window.config(state=tk.NORMAL)
        self.chat_window.insert(tk.END, f"{speaker}: {message}\n")
        self.chat_window.config(state=tk.DISABLED)
        self.chat_window.see(tk.END)

    def send_message(self, event=None):
        """
        Handle user input from the GUI entry box and generate chatbot response.
        """
        user_msg = self.input_box.get().strip()
        if not user_msg:
            return

        self.append_chat("You", user_msg)
        self.input_box.delete(0, tk.END)

        # Silence internal debug prints
        old_stdout = sys.stdout
        sys.stdout = io.StringIO()
        try:
            bot_response = self.persona.chat(user_msg)
        finally:
            sys.stdout = old_stdout

        self.append_chat(self.bot_name, bot_response)

        self.last_user_message = user_msg
        self.last_bot_response = bot_response

        self.update_visualizer()

    def send_feedback(self, feedback_value):
        """
        Send user feedback (+1/-1) to the Personality engine.
        """
        if self.last_user_message and self.last_bot_response:
            self.persona._automatic_evolution(
                self.last_user_message, self.last_bot_response, feedback_value
            )
            self.persona.save()
            self.update_visualizer()
            self.append_chat(self.bot_name, "Feedback recorded ✅")
        else:
            messagebox.showinfo("Info", "Send a message before giving feedback.")

    # ----------------------
    # Personality dropdown
    # ----------------------
    def switch_personality_dropdown(self, value):
        """
        Switch the active personality based on the dropdown selection.
        """
        try:
            self.persona.switch_personality(value)
            self.update_visualizer()
            self.append_chat(self.bot_name, f"Switched to {value}")
        except ValueError as e:
            messagebox.showerror("Error", str(e))

    # ----------------------
    # Dynamic weighted hybrid using sliders
    # ----------------------
    def dynamic_hybrid_dialog(self):
        """
        Open a dialog allowing the user to assign weights to multiple profiles
        using sliders and apply them as a weighted hybrid.
        """
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
            weights = {}
            for profile, slider in weight_sliders.items():
                val = slider.get()
                if val > 0:
                    weights[profile] = val
            if not weights:
                messagebox.showerror("Invalid Input", "At least one weight must be greater than 0")
                return
            try:
                self.persona.set_weighted_hybrid(weights)
                self.update_visualizer()
                self.append_chat(
                    self.bot_name,
                    f"Weighted hybrid active: {', '.join([f'{k}({v:.2f})' for k,v in weights.items()])}"
                )
                dialog.destroy()
            except ValueError as e:
                messagebox.showerror("Error", str(e))

        tk.Button(dialog, text="Apply", command=apply_weights).pack(pady=10)

    # ----------------------
    # Visualization
    # ----------------------
    def update_visualizer(self):
        """
        Refresh the personality visualization plot.
        """
        self.visualizer.update_history()
        self.canvas.draw()


if __name__ == "__main__":
    root = tk.Tk()
    app = PersonalityChatApp(root)
    root.mainloop()

