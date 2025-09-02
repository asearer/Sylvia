"""
Console visualization module using Rich.
Displays active profiles, weights, micro-personalities, and interaction stats.
"""

from rich.console import Console
from rich.table import Table
from rich.panel import Panel

class PersonalityVisualizer:
    """
    Provides a console-based visualization of the AI's personality.
    """

    def __init__(self, personality):
        """
        Args:
            personality: Instance of personality class
        """
        self.personality = personality
        self.console = Console()

    def show(self):
        """Render the current personality state in the console."""
        self.console.clear()

        # Active Profiles
        profile_table = Table(title="Active Profiles", show_header=True, header_style="bold magenta")
        profile_table.add_column("Profile")
        profile_table.add_column("Weight", justify="right")
        for name, weight in self.personality.active_profiles.items():
            profile_table.add_row(name, f"{weight:.2f}")

        # Micro-Personalities
        micro_table = Table(title="Micro-Personalities", show_header=True, header_style="bold cyan")
        micro_table.add_column("Name")
        micro_table.add_column("Weight", justify="right")
        micro_table.add_column("Quirks / Idioms")
        for name, data in self.personality.micro_personalities.items():
            if data["weight"] > 0.05:
                quirks = ", ".join(data["quirks"] + data["idioms"])
                micro_table.add_row(name, f"{data['weight']:.2f}", quirks[:50]+"..." if len(quirks) > 50 else quirks)

        # Stats Panel
        stats_panel = Panel(f"Interactions: {self.personality.interactions}\n"
                            f"Total words tracked: {len(self.personality.history_words)}",
                            title="Stats", border_style="green")

        # Render tables and panel
        self.console.print(profile_table)
        self.console.print(micro_table)
        self.console.print(stats_panel)
