"""
web.py

Provides a web interface for SylviaBot using FastAPI and Jinja2 templates.

WARNING: The current implementation uses a global in-memory chat_history, which is shared across all users and sessions. For production, use session-based or database-backed storage for chat history.

Features:
- Browser-based chat interface.
- Persistent in-memory conversation history for the current session.
- Integration with the SylviaBot chatbot module.
- Serves static assets (CSS, JS, images) from the 'static' folder.
"""

import os
from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from src.bot.sylvia import SylviaBot

# Initialize FastAPI app
app = FastAPI(title="Sylvia Chatbot Web Interface")

# Mount static files (CSS, JS, images)
# Static files are served at /static/ URL
app.mount("/static", StaticFiles(directory="static"), name="static")

# Set Jinja2 templates directory
templates = Jinja2Templates(directory=os.path.abspath(os.path.join(os.path.dirname(__file__), '../../templates')))

# Initialize the chatbot
bot = SylviaBot()

# In-memory chat history for the current session
# Each entry is a dictionary: {"user": user_input, "bot": bot_response}
chat_history = []

@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    """
    Render the main chat interface.

    Args:
        request (Request): FastAPI request object.

    Returns:
        TemplateResponse: Renders 'chat.html' template with current chat history.
    """
    return templates.TemplateResponse(
        "chat.html",
        {
            "request": request,
            "messages": chat_history  # Pass full message history to template
        }
    )

@app.post("/chat", response_class=HTMLResponse)
async def chat(request: Request, user_input: str = Form(...)):
    """
    Handle user input submitted from the web form and generate bot response.

    Args:
        request (Request): FastAPI request object.
        user_input (str): User's message from form submission.

    Returns:
        TemplateResponse: Renders 'chat.html' template including the new message.
    """
    # Generate bot response using SylviaBot
    response = bot.get_response(user_input)

    # Append the conversation pair to the in-memory chat history
    chat_history.append({"user": user_input, "bot": response})

    # Render the template with updated message history
    return templates.TemplateResponse(
        "chat.html",
        {
            "request": request,
            "messages": chat_history
        }
    )

@app.post("/reset", response_class=HTMLResponse)
async def reset_chat(request: Request):
    """
    Optional endpoint to reset the chat history.

    Args:
        request (Request): FastAPI request object.

    Returns:
        TemplateResponse: Renders 'chat.html' with empty message history.
    """
    chat_history.clear()  # Clear in-memory conversation
    return templates.TemplateResponse(
        "chat.html",
        {
            "request": request,
            "messages": chat_history
        }
    )
