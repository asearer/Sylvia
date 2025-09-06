"""
web.py

Provides a web interface for SylviaBot using FastAPI and Jinja2 templates.

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

# Import SylviaBot from sylvia-app bot module
from src.bot.sylvia import SylviaBot

# Initialize FastAPI app
app = FastAPI(title="Sylvia Chatbot Web Interface")

# Mount static files (CSS, JS, images)
app.mount("/static", StaticFiles(directory="static"), name="static")

# Set Jinja2 templates directory
templates = Jinja2Templates(directory=os.path.abspath(os.path.join(os.path.dirname(__file__), '../../templates')))

# Initialize the chatbot
bot = SylviaBot()

# In-memory chat history for the current session
chat_history = []

@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    """Render the main chat interface."""
    return templates.TemplateResponse(
        "chat.html",
        {
            "request": request,
            "messages": chat_history
        }
    )

@app.post("/chat", response_class=HTMLResponse)
async def chat(request: Request, user_input: str = Form(...)):
    """Handle user input and generate bot response."""
    # Handle /switch command
    if user_input.lower().startswith("/switch"):
        parts = user_input.split()
        if len(parts) > 1:
            bot.switch_personality(parts[1])
            response = f"Switched to {parts[1]}"
            chat_history.append({"user": user_input, "bot": response})
            return templates.TemplateResponse("chat.html", {"request": request, "messages": chat_history})

    # Handle /hybrid command
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
                    return templates.TemplateResponse("chat.html", {"request": request, "messages": chat_history})
            bot.set_weighted_hybrid(weights)
            response = f"Weighted hybrid active: {', '.join([f'{k}({v})' for k,v in weights.items()])}"
            chat_history.append({"user": user_input, "bot": response})
            return templates.TemplateResponse("chat.html", {"request": request, "messages": chat_history})

    # Normal message
    response = bot.get_response(user_input)
    chat_history.append({"user": user_input, "bot": response})
    return templates.TemplateResponse("chat.html", {"request": request, "messages": chat_history})

@app.post("/reset", response_class=HTMLResponse)
async def reset_chat(request: Request):
    """Reset the chat history."""
    chat_history.clear()
    return templates.TemplateResponse("chat.html", {"request": request, "messages": chat_history})
