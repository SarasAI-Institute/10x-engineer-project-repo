"""PromptLab API Server.

This is the entry point for the PromptLab FastAPI application.
It starts an Uvicorn ASGI server to handle HTTP requests.

Usage:
    python main.py

Configuration:
    - Host: 0.0.0.0 (accessible from all network interfaces)
    - Port: 8000
    - Reload: True (auto-reload on code changes for development)

Endpoints:
    - API Documentation: http://localhost:8000/docs
    - OpenAPI Schema: http://localhost:8000/openapi.json
    - Health Check: http://localhost:8000/health
"""

import uvicorn
from app.api import app

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
