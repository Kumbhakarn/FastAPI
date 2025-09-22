"""
gzip_middleware.py — FastAPI Application with GZip Middleware

Purpose:
--------
This file demonstrates how to enable GZip compression in a FastAPI application.
GZip middleware compresses responses that exceed a certain size, reducing
network bandwidth and improving performance for clients.

Why important?
--------------
- Improves API response times for large payloads.
- Reduces data transfer size over the network.
- Works automatically for responses larger than the configured minimum size.

"""

from fastapi import FastAPI
from starlette.middleware.gzip import GZipMiddleware

# -------------------------------------------------------------------------
# Initialize FastAPI app
# -------------------------------------------------------------------------
app = FastAPI(
    title="FastAPI with GZip Middleware",
    description="An example FastAPI app with GZip response compression enabled.",
    version="1.0.0"
)

# -------------------------------------------------------------------------
# Add GZip Middleware
# -------------------------------------------------------------------------
app.add_middleware(
    GZipMiddleware,
    minimum_size=1000  # Only compress responses larger than 1000 bytes
)

# -------------------------------------------------------------------------
# Example endpoint
# -------------------------------------------------------------------------
@app.get("/")
def root():
    """
    Root endpoint to test GZip compression.
    Returns a sample large payload to trigger compression.
    """
    sample_data = "Hello World! " * 200  # Example large response
    return {"message": sample_data}
