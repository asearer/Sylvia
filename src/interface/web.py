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
    """
    # Handle special commands
    if user_input.lower().startswith("/switch"):
        parts = user_input.split()
        if len(parts) > 1:
            bot.switch_personality(parts[1])
            response = f"Switched to {parts[1]}"
            chat_history.append({"user": user_input, "bot": response})
            return templates.TemplateResponse(
                "chat.html",
                {
                    "request": request,
                    "messages": chat_history
                }
            )
    if user_input.lower().startswith("/hybrid"):
        parts = user_input.split()
        if len(parts) > 1:
            weights = {}
            for pair in parts[1].split(","):
                try:
                    name, w = pair.split(":")
                    weights[name] = float(w)
                except:
                    response = f"Invalid format: {pair}. Use Name:Weight"
                    chat_history.append({"user": user_input, "bot": response})
                    return templates.TemplateResponse(
                        "chat.html",
                        {
                            "request": request,
                            "messages": chat_history
                        }
                    )
            bot.set_weighted_hybrid(weights)
            response = f"Weighted hybrid active: {', '.join([f'{k}({v})' for k,v in weights.items()])}"
            chat_history.append({"user": user_input, "bot": response})
            return templates.TemplateResponse(
                "chat.html",
                {
                    "request": request,
                    "messages": chat_history
                }
            )
    # Generate bot response using SylviaBot
    response = bot.get_response(user_input)
    chat_history.append({"user": user_input, "bot": response})
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
