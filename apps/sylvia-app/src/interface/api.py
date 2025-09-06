"""
api.py

FastAPI REST interface for SylviaBot.
"""

from fastapi import FastAPI
from pydantic import BaseModel
from src.bot.sylvia import SylviaBot

app = FastAPI(title="Sylvia Chatbot API")
bot = SylviaBot()

class Message(BaseModel):
    user_input: str
    feedback: int = None
    switch_profile: str = None
    hybrid_weights: dict = None

@app.post("/chat")
def chat(msg: Message):
    """Send a message to SylviaBot via API."""
    if msg.switch_profile:
        bot.switch_personality(msg.switch_profile)
    if msg.hybrid_weights:
        bot.set_weighted_hybrid(msg.hybrid_weights)
    response = bot.get_response(msg.user_input, feedback=msg.feedback)
    return {"response": response}
