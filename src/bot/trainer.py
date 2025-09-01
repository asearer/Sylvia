"""
trainer.py

Handles additional training routines for SylviaBot, including
dynamic learning from user feedback.
"""

import yaml
from pathlib import Path

def save_conversation_to_yaml(user_input, bot_response, file_path="./data/custom_corpus.yml"):
    """
    Append a new conversation pair to the YAML training corpus.

    Args:
        user_input (str): User message.
        bot_response (str): Bot's response.
        file_path (str): Path to YAML corpus file.
    """
    Path(file_path).parent.mkdir(parents=True, exist_ok=True)

    conversation = {
        "conversations": [
            [user_input, bot_response]
        ]
    }

    if Path(file_path).exists():
        with open(file_path, "r", encoding="utf-8") as f:
            existing_data = yaml.safe_load(f) or {}
        existing_data.setdefault("conversations", []).extend(conversation["conversations"])
    else:
        existing_data = conversation

    with open(file_path, "w", encoding="utf-8") as f:
        yaml.safe_dump(existing_data, f)
