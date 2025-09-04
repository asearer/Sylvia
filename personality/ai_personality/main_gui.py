"""
main_gui.py

Fully GUI-only chat interface with live plots using PersonalityGUIVisualizer.
Side-by-side layout: visualization + chat, with instant updates.
"""

import sys
import os
import tkinter as tk
from tkinter import simpledialog, messagebox, scrolledtext
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import io
from pathlib import Path

# Add ai_personality to sys.path for imports
sys.path.append(os.path.join(os.path.dirname(__file__)))

from personality.personality import Personality
from personality.visualizer_gui import PersonalityGUIVisualizer

class PersonalityChatApp:
    def __init__(self, master):
        self.master = master
        master.title("Sylvia Chatbot")

        # Locate profiles.json relative to this file
        profiles_path = Path(__file__).parent / "personality" / "profiles.json"

        # Initialize personality and visualizer
        self.persona = Personality("astronaut", profiles_path=profiles_path, evolving=True)
        self.visualizer = PersonalityGUIVisualizer(self.persona)

        # Main frame for side-by-side layout
        main_frame = tk.Frame(master)
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Left frame: Visualization
        viz_frame = tk.Frame(main_frame)
        viz_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.canvas = FigureCanvasTkAgg(self.visualizer.fig, master=viz_frame)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        self.canvas.draw()

        # Right frame: Chat interface
        chat_frame = tk.Frame(main_frame)
        chat_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.chat_window = scrolledtext.ScrolledText(chat_frame, wrap=tk.WORD, width=50, height=20, state=tk.DISABLED)
        self.chat_window.pack(padx=5, pady=5, fill=tk.BOTH, expand=True)

        # Input frame
        input_frame = tk.Frame(chat_frame)
        input_frame.pack(padx=5, pady=5, fill=tk.X)

        self.input_box = tk.Entry(input_frame)
        self.input_box.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0,5))
        self.input_box.bind("<Return>", self.send_message)

        self.send_btn = tk.Button(input_frame, text="Send", command=self.send_message)
        self.send_btn.pack(side=tk.LEFT)

        # Buttons for personality actions
        control_frame = tk.Frame(chat_frame)
        control_frame.pack(pady=5)

        self.switch_btn = tk.Button(control_frame, text="Switch Personality", command=self.switch_personality)
        self.switch_btn.pack(side=tk.LEFT, padx=5)

        self.hybrid_btn = tk.Button(control_frame, text="Weighted Hybrid", command=self.set_hybrid)
        self.hybrid_btn.pack(side=tk.LEFT, padx=5)

        # Feedback buttons
        self.feedback_frame = tk.Frame(chat_frame)
        self.feedback_frame.pack(pady=5)

        self.positive_fb = tk.Button(self.feedback_frame, text="👍", command=lambda: self.send_feedback(1))
        self.positive_fb.pack(side=tk.LEFT, padx=5)
        self.negative_fb = tk.Button(self.feedback_frame, text="👎", command=lambda: self.send_feedback(-1))
        self.negative_fb.pack(side=tk.LEFT, padx=5)

        # Last message tracking for feedback
        self.last_user_message = None
        self.last_bot_response = None

        # Keyboard shortcut to quit
        master.bind("<Escape>", lambda e: master.quit())

        # Initial visualization update
        self.update_visualizer()

    def append_chat(self, speaker, message):
        self.chat_window.config(state=tk.NORMAL)
        self.chat_window.insert(tk.END, f"{speaker}: {message}\n")
        self.chat_window.config(state=tk.DISABLED)
        self.chat_window.see(tk.END)

    def send_message(self, event=None):
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

        self.append_chat(", ".join(self.persona.active_profiles) + " AI", bot_response)

        self.last_user_message = user_msg
        self.last_bot_response = bot_response

        self.update_visualizer()

    def send_feedback(self, feedback_value):
        if self.last_user_message and self.last_bot_response:
            self.persona._automatic_evolution(self.last_user_message, self.last_bot_response, feedback_value)
            self.persona.save()
            self.update_visualizer()
            self.append_chat("System", "Feedback recorded ✅")
        else:
            messagebox.showinfo("Info", "Send a message before giving feedback.")

    def switch_personality(self):
        new_profile = simpledialog.askstring("Switch Personality", "Enter new personality profile name:")
        if new_profile:
            try:
                self.persona.switch_personality(new_profile)
                self.update_visualizer()
                self.append_chat("System", f"Switched to {new_profile}")
            except ValueError as e:
                messagebox.showerror("Error", str(e))

    def set_hybrid(self):
        weights_input = simpledialog.askstring(
            "Weighted Hybrid",
            "Enter weights as Name:Weight, comma-separated (e.g., astronaut:0.7,chef:0.3):"
        )
        if weights_input:
            weights = {}
            for pair in weights_input.split(","):
                try:
                    name, w = pair.split(":")
                    weights[name.strip()] = float(w)
                except:
                    messagebox.showerror("Error", f"Invalid format: {pair}")
                    return
            try:
                self.persona.set_weighted_hybrid(weights)
                self.update_visualizer()
                self.append_chat("System", f"Weighted hybrid active: {', '.join([f'{k}({v})' for k,v in weights.items()])}")
            except ValueError as e:
                messagebox.showerror("Error", str(e))

    def update_visualizer(self):
        self.visualizer.update_history()
        self.canvas.draw()

if __name__ == "__main__":
    root = tk.Tk()
    app = PersonalityChatApp(root)
    root.mainloop()



