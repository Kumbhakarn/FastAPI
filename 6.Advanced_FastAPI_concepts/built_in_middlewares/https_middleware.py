"""
https_middleware.py — FastAPI Application with HTTPS Redirection Middleware

Purpose:
--------
This file demonstrates how to enable HTTPS redirection in a FastAPI application.
The HTTPSRedirectMiddleware automatically redirects incoming HTTP requests
to HTTPS, ensuring secure communication between clients and the API.

Why important?
--------------
- Enforces encrypted connections, improving security.
- Protects sensitive data in transit (e.g., API keys, user info).
- Simple way to ensure all traffic uses HTTPS without changing the API logic.

"""

from fastapi import FastAPI
from starlette.middleware.httpsredirect import HTTPSRedirectMiddleware

# -------------------------------------------------------------------------
# Initialize FastAPI app
# -------------------------------------------------------------------------
app = FastAPI(
    title="FastAPI with HTTPS Redirection",
    description="An example FastAPI app that automatically redirects HTTP requests to HTTPS.",
    version="1.0.0"
)

# -------------------------------------------------------------------------
# Add HTTPS Redirect Middleware
# -------------------------------------------------------------------------
app.add_middleware(
    HTTPSRedirectMiddleware  # Redirect all HTTP requests to HTTPS
)

# -------------------------------------------------------------------------
# Example endpoint
# -------------------------------------------------------------------------
@app.get("/")
def root():
    """
    Root endpoint to test HTTPS redirection.
    If accessed via HTTP, the request will be redirected to HTTPS automatically.
    """
    return {"message": "HTTPS redirect middleware is active 🚀"}
