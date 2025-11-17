"""
main.py

Entry point for SylviaBot. Allows selection between CLI, API, and GUI interfaces.
"""

import argparse
import uvicorn

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run SylviaBot")
    parser.add_argument(
        "--mode", choices=["cli", "api", "gui"], default="cli",
        help="Select interface mode (CLI, API, GUI)"
    )
    parser.add_argument(
        "--backend",
        choices=["stub", "local", "api"],
        default="stub",
        help="Select backend type (stub/local/api)"
    )
    args = parser.parse_args()

    if args.mode == "cli":
        from src.interface.cli import start_cli
        start_cli(backend=args.backend)

    elif args.mode == "api":
        uvicorn.run("src.interface.api:app", host="0.0.0.0", port=8000, reload=True)

    elif args.mode == "gui":
        from src.interface.gui import start_gui
        start_gui(backend=args.backend)


