"""
main.py

Entry point for SylviaBot. Allows selection between CLI and API interface.
"""

import argparse
from src.interface import cli
import uvicorn

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run SylviaBot")
    parser.add_argument("--mode", choices=["cli", "api"], default="cli", help="Interface mode")
    parser.add_argument("--model", type=str, help="Path to trained model or corpus")
    args = parser.parse_args()

    if args.mode == "cli":
        cli.start_cli(model_path=args.model)
    elif args.mode == "api":
        uvicorn.run("src.interface.api:app", host="0.0.0.0", port=8000, reload=True)
