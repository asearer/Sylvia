"""
api.py

Provides a FastAPI interface for SylviaBot to enable web or
multi-user interaction.
"""

from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional, Dict
from sylvia.bot.sylvia import SylviaBot
import logging

logging.basicConfig(level=logging.INFO)

app = FastAPI(title="Sylvia Chatbot API")

bot = SylviaBot()  # Initialize default bot instance

class Message(BaseModel):
    user_input: str
    feedback: Optional[int] = None
    switch_profile: Optional[str] = None
    hybrid_weights: Optional[Dict[str, float]] = None

@app.post("/chat")
def chat(msg: Message):
    """
    Endpoint to send a message to Sylvia and receive a response.

    Handles optional:
    - Personality switching
    - Weighted hybrid profiles
    - Feedback (+1/-1)
    """
    try:
        if msg.switch_profile:
            bot.switch_personality(msg.switch_profile)
            logging.info(f"Switched profile to {msg.switch_profile}")
        if msg.hybrid_weights:
            bot.set_weighted_hybrid(msg.hybrid_weights)
            logging.info(f"Set hybrid weights: {msg.hybrid_weights}")
        response = bot.get_response(msg.user_input, feedback=msg.feedback)
        logging.info(f"User input: {msg.user_input} | Response: {response}")
        return {"response": response, "active_profiles": bot.personality.active_profiles}
    except ValueError as e:
        return {"error": str(e)}
