"""
main.py

Entry point for SylviaBot. Allows selection between CLI, GUI, and API interfaces.
Refactor-ready for monorepo structure.
"""

import argparse

# Import SylviaBot and interfaces
from sylvia.bot.sylvia import SylviaBot
from sylvia.interface.cli import start_cli
from sylvia.interface.gui import start_gui

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run SylviaBot")
    parser.add_argument(
        "--mode",
        choices=["cli", "gui", "api"],
        default="cli",
        help="Interface mode: cli, gui, or api"
    )
    parser.add_argument(
        "--model",
        type=str,
        default=None,
        help="Path to trained model or corpus (optional)"
    )
    args = parser.parse_args()

    # Initialize SylviaBot instance
    bot = SylviaBot(model=args.model)

    # Launch chosen interface
    if args.mode == "cli":
        start_cli(bot)
    elif args.mode == "gui":
        start_gui(bot)
    elif args.mode == "api":
        # Optional API launch placeholder
        import uvicorn
        uvicorn.run("sylvia.interface.api:app", host="0.0.0.0", port=8000, reload=True)
