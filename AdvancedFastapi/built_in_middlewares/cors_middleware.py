"""
cors_middleware.py — FastAPI Application with CORS Middleware

Purpose:
--------
This file demonstrates how to configure **Cross-Origin Resource Sharing (CORS)**
in FastAPI. CORS middleware is essential when your frontend (e.g., React, Angular,
Vue) is hosted on a different domain or port than your backend API.

Why important?
--------------
- Prevents browser errors when frontend and backend run on different origins.
- Allows controlled cross-origin requests (security).
- Defines which origins, methods, and headers are permitted.

"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# -------------------------------------------------------------------------
# Initialize FastAPI app
# -------------------------------------------------------------------------
app = FastAPI(
    title="FastAPI with CORS Middleware",
    description="An example FastAPI app with CORS enabled for frontend integration.",
    version="1.0.0"
)

# -------------------------------------------------------------------------
# Configure CORS Middleware
# -------------------------------------------------------------------------

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://my-frontend.com",  # Production frontend
        "http://localhost:3000"     # Local development frontend
    ],
    allow_credentials=True,          # Allow cookies/auth headers
    allow_methods=["GET", "POST", "PUT", "DELETE"],  # Allowed HTTP methods
    allow_headers=["*"]              # Allow all headers (can restrict if needed)
)

# -------------------------------------------------------------------------
# Define Endpoints (for testing CORS setup)
# -------------------------------------------------------------------------
@app.get("/")
def root():
    """
    Root endpoint to test if CORS is working.
    """
    return {"message": "CORS-enabled FastAPI app is running 🚀"}
