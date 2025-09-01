"""
api.py

Provides a FastAPI interface for SylviaBot to enable web or
multi-user interaction.
"""

from fastapi import FastAPI
from pydantic import BaseModel
from bot.sylvia import SylviaBot

app = FastAPI(title="Sylvia Chatbot API")

bot = SylviaBot()  # Initialize default bot instance

class Message(BaseModel):
    user_input: str

@app.post("/chat")
def chat(msg: Message):
    """
    Endpoint to send a message to Sylvia and receive a response.

    Args:
        msg (Message): User input message.

    Returns:
        dict: Bot's response.
    """
    response = bot.get_response(msg.user_input)
    return {"response": response}
