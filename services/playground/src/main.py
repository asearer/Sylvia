"""
Sylvia Playground Service
-------------------------
Microservice for safe execution of code snippets.
Provides an API to run Python, Bash, and JavaScript code with timeouts and basic safety checks.
"""

import uvicorn
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional, Dict, Any
from contextlib import asynccontextmanager
import logging
import sys

from .executor import CodeREPL

def setup_logger(name: str = "playground"):
    """
    Configure and return a standardized logger.
    """
    logger = logging.getLogger(name)
    if not logger.handlers:
        handler = logging.StreamHandler(sys.stdout)
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        logger.setLevel(logging.INFO)
    return logger

logger = setup_logger()

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Playground Service starting up...")
    yield
    logger.info("Playground Service shutting down...")

app = FastAPI(title="Sylvia Playground Service", lifespan=lifespan)
repl = CodeREPL()

class ExecutionRequest(BaseModel):
    code: str
    language: str = "python"
    timeout: int = 5

class ExecutionResponse(BaseModel):
    output: str
    error: Optional[str] = None
    exit_code: int

@app.post("/execute", response_model=ExecutionResponse)
async def execute_code(request: ExecutionRequest):
    """
    Execute a code snippet.
    """
    try:
        result = await repl.execute(request.code, request.language, request.timeout)
        return result
    except Exception as e:
        logger.error(f"Error during execution request: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
def health_check():
    return {"status": "online", "service": "playground"}

if __name__ == "__main__":
    # Allow configuration via args in a real deployment
    uvicorn.run(app, host="0.0.0.0", port=5002)
