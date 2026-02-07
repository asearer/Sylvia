"""
visualizer_gui.py - Provides a minimal Tkinter GUI for visualizing Personality objects.

Expandable for use as a dashboard in-personality editors or trainers.
"""
import tkinter as tk
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
from .visualizer import PersonalityVisualizer
from .personality import Personality

class PersonalityVisualizerGUI(tk.Tk):
    """
    GUI application for visual exploration of Personality traits.
    Allows loading different personalities and viewing their trait profiles.
    """
    def __init__(self, personality: Personality):
        super().__init__()
        self.title(f"Personality Visualizer: {personality.name}")
        self.geometry("600x400")
        self.personality = personality
        self._setup_widgets()
        self._draw_plot()

    def _setup_widgets(self):
        frm = ttk.Frame(self)
        frm.pack(fill=tk.BOTH, expand=1)
        self.fig, self.ax = plt.subplots(figsize=(5,3))
        self.canvas = FigureCanvasTkAgg(self.fig, master=frm)
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
        # Optionally: Add controls for loading/editing personality here

    def _draw_plot(self):
        self.ax.clear()
        PersonalityVisualizer.plot_traits(self.personality, ax=self.ax, title=self.personality.name)
        self.canvas.draw()

# Example usage
if __name__ == "__main__":
    p = Personality("curious", {"openness": 0.91, "discipline": 0.65, "sociability": 0.5})
    app = PersonalityVisualizerGUI(p)
    app.mainloop()
