"""
Matplotlib-based GUI visualization for AI personality dynamics.
Displays profile weights and micro-personality counts over time.
"""

import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from collections import defaultdict

class PersonalityGUIVisualizer:
    """
    Provides a live, updating graph of personality state and evolution.
    """

    def __init__(self, personality):
        """
        Args:
            personality: Instance of personality
        """
        self.personality = personality
        self.weights_history = defaultdict(list)
        self.interactions_history = []
        self.micro_count_history = []

        # Initialize Matplotlib figure
        self.fig, (self.ax1, self.ax2) = plt.subplots(2, 1, figsize=(10, 6))
        self.ax1.set_title("Profile Weights Over Time")
        self.ax1.set_xlabel("Interaction")
        self.ax1.set_ylabel("Weight")
        self.ax1.set_ylim(0, 1.0)

        self.ax2.set_title("Micro-Personalities Over Time")
        self.ax2.set_xlabel("Interaction")
        self.ax2.set_ylabel("Count")

    def update_history(self):
        """Update history with current personality weights and micro-personality count."""
        self.interactions_history.append(self.personality.interactions)
        for profile, weight in self.personality.active_profiles.items():
            self.weights_history[profile].append(weight)
        micro_count = sum(1 for mp in self.personality.micro_personalities.values() if mp["weight"] > 0.05)
        self.micro_count_history.append(micro_count)

    def animate(self, i):
        """Animation function for FuncAnimation."""
        self.ax1.clear()
        self.ax2.clear()
        self.ax1.set_title("Profile Weights Over Time")
        self.ax1.set_xlabel("Interaction")
        self.ax1.set_ylabel("Weight")
        self.ax1.set_ylim(0, 1.0)
        self.ax2.set_title("Micro-Personalities Over Time")
        self.ax2.set_xlabel("Interaction")
        self.ax2.set_ylabel("Count")

        # Plot profile weights
        for profile, weights in self.weights_history.items():
            self.ax1.plot(self.interactions_history, weights, label=profile, marker='o')

        # Plot micro-personality count
        self.ax2.plot(self.interactions_history, self.micro_count_history, color='purple', marker='x')

        self.ax1.legend(loc='upper right')

    def start(self):
        """Start the live visualization."""
        self.ani = FuncAnimation(self.fig, self.animate, interval=1000)
        plt.tight_layout()
        plt.show()
