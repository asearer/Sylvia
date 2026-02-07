"""
Entrypoint for the Code Analysis Service.

Provides:
- REST API for code analysis
- Health check endpoint
- CLI demo fallback

Dependencies:
    pip install fastapi uvicorn
"""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from analyzer import CodeAnalyzer
import uvicorn

# -----------------------------
# FastAPI app initialization
# -----------------------------
app = FastAPI(title="Sylvia Code Analysis Service")
analyzer = CodeAnalyzer()

# -----------------------------
# Request/Response Models
# -----------------------------
class CodeRequest(BaseModel):
    code: str


class AnalysisResponse(BaseModel):
    structure: list
    dependencies: list
    issues: list


class HealthResponse(BaseModel):
    module: str
    status: str
    model_loaded: bool


# -----------------------------
# API Endpoints
# -----------------------------
@app.post("/analyze", response_model=AnalysisResponse)
def analyze_code(request: CodeRequest):
    if not request.code.strip():
        raise HTTPException(status_code=400, detail="Code snippet cannot be empty")
    result = analyzer.analyze_code(request.code)
    return result


@app.get("/health", response_model=HealthResponse)
def health_check():
    return analyzer.health_check()


# -----------------------------
# CLI fallback
# -----------------------------
def cli_demo():
    test_code = "def hello():\n    print('Hello World')"
    result = analyzer.analyze_code(test_code)
    print("Analysis result:", result)
    print("Health check:", analyzer.health_check())


# -----------------------------
# Entrypoint
# -----------------------------
if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Run Code Analysis Service")
    parser.add_argument(
        "--cli", action="store_true", help="Run CLI demo instead of API"
    )
    parser.add_argument(
        "--host", type=str, default="127.0.0.1", help="API host"
    )
    parser.add_argument(
        "--port", type=int, default=8000, help="API port"
    )
    args = parser.parse_args()

    if args.cli:
        cli_demo()
    else:
        uvicorn.run(app, host=args.host, port=args.port)
