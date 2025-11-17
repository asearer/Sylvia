"""
web.py

FastAPI web interface using Jinja2 templates for SylviaBot.
"""

import os
from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from src.bot.sylvia import SylviaBot

# Initialize app
app = FastAPI(title="Sylvia Chatbot Web Interface")
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory=os.path.abspath(os.path.join(os.path.dirname(__file__), '../../templates')))

bot = SylviaBot()
chat_history = []

@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    """Render the main chat page."""
    return templates.TemplateResponse("chat.html", {"request": request, "messages": chat_history})

@app.post("/chat", response_class=HTMLResponse)
async def chat(request: Request, user_input: str = Form(...)):
    """Process user input and return bot response."""
    if user_input.lower().startswith("/switch"):
        parts = user_input.split()
        if len(parts) > 1:
            bot.switch_personality(parts[1])
            response = f"Switched to {parts[1]}"
            chat_history.append({"user": user_input, "bot": response})
            return templates.TemplateResponse("chat.html", {"request": request, "messages": chat_history})

    if user_input.lower().startswith("/hybrid"):
        parts = user_input.split()
        if len(parts) > 1:
            weights = {}
            for pair in parts[1].split(","):
                try:
                    name, w = pair.split(":")
                    weights[name] = float(w)
                except ValueError:
                    response = f"Invalid format: {pair}. Use Name:Weight"
                    chat_history.append({"user": user_input, "bot": response})
                    return templates.TemplateResponse("chat.html", {"request": request, "messages": chat_history})
            bot.set_weighted_hybrid(weights)
            response = f"Weighted hybrid active: {', '.join([f'{k}({v})' for k,v in weights.items()])}"
            chat_history.append({"user": user_input, "bot": response})
            return templates.TemplateResponse("chat.html", {"request": request, "messages": chat_history})

    response = bot.get_response(user_input)
    chat_history.append({"user": user_input, "bot": response})
    return templates.TemplateResponse("chat.html", {"request": request, "messages": chat_history})

@app.post("/reset", response_class=HTMLResponse)
async def reset_chat(request: Request):
    """Reset chat history."""
    chat_history.clear()
    return templates.TemplateResponse("chat.html", {"request": request, "messages": chat_history})
