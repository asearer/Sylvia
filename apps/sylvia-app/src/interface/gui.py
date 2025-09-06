# src/interface/gui.py

"""
gui.py

Tkinter GUI for SylviaBot using selectable backends.
Allows sending messages, switching profiles, and setting weighted hybrid.
"""

import sys
import tkinter as tk
from tkinter import scrolledtext, StringVar, messagebox
import time
import io
from typing import Optional, Dict

# -----------------------------
# Import SylviaBot stub
# -----------------------------
from src.bot.sylvia import SylviaBot

# -----------------------------
# Stub visualizer (no plotting)
# -----------------------------
class StubVisualizer:
    """Temporary visualizer without Matplotlib plotting."""
    def __init__(self, personality=None):
        self.personality = personality

    def update_history(self):
        """Dummy method, does nothing."""
        pass

    def animate(self, i):
        """Dummy method, does nothing."""
        pass

# -----------------------------
# GUI function
# -----------------------------
def start_gui(backend: str = "stub") -> None:
    """Launch the SylviaBot GUI with a selectable backend."""
    bot = SylviaBot(backend=backend)
    visualizer = StubVisualizer(bot.personality)

    root = tk.Tk()
    root.title(f"Sylvia Chatbot GUI ({backend} backend)")
    root.geometry("800x500")

    # Chat display
    chat_display = scrolledtext.ScrolledText(root, state='disabled', width=60, height=20, wrap=tk.WORD)
    chat_display.grid(row=0, column=0, columnspan=2, padx=10, pady=10, sticky='nsew')

    # User input
    user_input = StringVar()
    input_entry = tk.Entry(root, textvariable=user_input, width=50)
    input_entry.grid(row=1, column=0, padx=10, pady=5, sticky='ew')
    input_entry.focus_set()

    def display_response(response: str) -> None:
        """Append message to chat display."""
        chat_display.config(state='normal')
        chat_display.insert(tk.END, f"{response}\n")
        chat_display.config(state='disabled')
        chat_display.see(tk.END)

    def send_message(event: Optional[tk.Event] = None) -> None:
        """Process user input and generate bot response."""
        msg = user_input.get().strip()
        if not msg:
            return
        chat_display.config(state='normal')
        chat_display.insert(tk.END, f"You: {msg}\n")
        chat_display.config(state='disabled')
        chat_display.see(tk.END)
        user_input.set("")
        input_entry.focus_set()

        # Handle commands
        if msg.lower().startswith("/switch"):
            parts = msg.split()
            if len(parts) > 1:
                bot.switch_personality(parts[1])
                response = f"Switched to {parts[1]}"
                visualizer.update_history()
                display_response(response)
                return

        if msg.lower().startswith("/hybrid"):
            parts = msg.split()
            if len(parts) > 1:
                weights: Dict[str, float] = {}
                for pair in parts[1].split(","):
                    try:
                        name, w = pair.split(":")
                        weights[name] = float(w)
                    except ValueError:
                        display_response(f"Invalid format: {pair}. Use Name:Weight")
                        return
                bot.set_weighted_hybrid(weights)
                response = f"Weighted hybrid active: {', '.join(weights.keys())}"
                visualizer.update_history()
                display_response(response)
                return

        if msg.lower() in ["quit", "exit"]:
            root.quit()
            return

        # Generate bot response
        start_time = time.time()
        old_stdout = sys.stdout
        sys.stdout = io.StringIO()
        try:
            response = bot.get_response(msg)
            debug_output = sys.stdout.getvalue()
        finally:
            sys.stdout = old_stdout
        elapsed = time.time() - start_time

        display_response(f"{', '.join(bot.active_profiles)} AI: {response}")
        if debug_output.strip():
            display_response(f"[DEBUG]: {debug_output.strip()}")
        display_response(f"[Time: {elapsed:.2f}s]")
        visualizer.update_history()

    input_entry.bind("<Return>", send_message)
    send_button = tk.Button(root, text="Send", command=send_message)
    send_button.grid(row=1, column=1, padx=5, pady=5)

    root.mainloop()

