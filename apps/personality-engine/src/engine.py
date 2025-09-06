"""
engine.py

Standalone entry point for the Personality Engine.
Can be run as CLI or (optionally) launch GUI.
"""

import argparse
from src.console_chat import main as console_main
# from src.gui import main as gui_main  # Uncomment when GUI is implemented

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run Personality Engine")
    parser.add_argument("--mode", choices=["cli", "gui"], default="cli")
    args = parser.parse_args()

    if args.mode == "cli":
        console_main()
    elif args.mode == "gui":
        # gui_main()
        print("GUI not implemented yet")
