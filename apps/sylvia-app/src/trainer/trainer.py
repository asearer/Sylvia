"""
trainer.py

Handles additional training routines for SylviaBot, including
dynamic learning from user feedback.
"""

import yaml
from pathlib import Path
from typing import Optional


def save_conversation_to_yaml(
    user_input: str,
    bot_response: str,
    file_path: str = "./data/custom_corpus.yml"
) -> Path:
    """
    Append a new conversation pair to the YAML training corpus.

    Args:
        user_input (str): User message.
        bot_response (str): Bot's response.
        file_path (str, optional): Path to YAML corpus file. Defaults to "./data/custom_corpus.yml".

    Returns:
        Path: Path to the YAML file where data was saved.
    """
    file_path = Path(file_path).resolve()
    file_path.parent.mkdir(parents=True, exist_ok=True)

    conversation = {
        "conversations": [
            [user_input, bot_response]
        ]
    }

    if file_path.exists():
        with open(file_path, "r", encoding="utf-8") as f:
            existing_data = yaml.safe_load(f) or {}
        existing_data.setdefault("conversations", []).extend(conversation["conversations"])
    else:
        existing_data = conversation

    with open(file_path, "w", encoding="utf-8") as f:
        yaml.safe_dump(existing_data, f, sort_keys=False, allow_unicode=True)

    return file_path
