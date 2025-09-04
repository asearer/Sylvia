"""
api.py

Provides a FastAPI interface for SylviaBot to enable web or
multi-user interaction.
"""

from fastapi import FastAPI
from pydantic import BaseModel
from src.bot.sylvia import SylviaBot

app = FastAPI(title="Sylvia Chatbot API")

bot = SylviaBot()  # Initialize default bot instance

class Message(BaseModel):
    user_input: str
    feedback: int = None  # Optional feedback (+1 or -1)
    switch_profile: str = None  # Optional profile switch
    hybrid_weights: dict = None  # Optional hybrid weights

@app.post("/chat")
def chat(msg: Message):
    """
    Endpoint to send a message to Sylvia and receive a response.
    """
    if msg.switch_profile:
        bot.switch_personality(msg.switch_profile)
    if msg.hybrid_weights:
        bot.set_weighted_hybrid(msg.hybrid_weights)
    response = bot.get_response(msg.user_input, feedback=msg.feedback)
    return {"response": response}
