"""
FastAPI Custom Middleware Example
=================================

This file demonstrates how to create and use **multiple custom middlewares** in FastAPI
by extending Starlette's `BaseHTTPMiddleware`.

Middleware in FastAPI/Starlette allows you to execute logic before and/or after 
a request is processed by your application. They are particularly useful for:
    - Logging request/response details
    - Measuring performance
    - Handling authentication/security
    - Adding or modifying headers
    - Error handling

Middlewares implemented here:
-----------------------------
1. TimerMiddleware:
   - Measures how long each request takes to be processed.
   - Logs the duration in seconds.

2. LoggingMiddleware:
   - Logs HTTP method, URL path, and client IP of each request.
   - Useful for debugging and request auditing.

Flow of Execution:
------------------
1. Request enters the application.
2. LoggingMiddleware runs → logs method, path, and client IP.
3. TimerMiddleware runs → starts timing.
4. Endpoint executes.
5. TimerMiddleware finishes timing → logs execution duration.
6. Response is returned to the client.

Usage:
------
- Run the application with: `uvicorn filename:app --reload`
- Access `http://127.0.0.1:8000/hello`
- Console will show request logs and processing times.

"""

import time
from fastapi import FastAPI, Request
from starlette.middleware.base import BaseHTTPMiddleware

# Initialize FastAPI app
app = FastAPI()


class TimerMiddleware(BaseHTTPMiddleware):
    """
    Middleware to measure request processing time.

    Inherits:
        BaseHTTPMiddleware (Starlette) - provides a structure for creating custom middlewares.

    Methods:
        dispatch(request, call_next):
            - Records the start time
            - Processes the request by calling the next handler
            - Calculates total duration
            - Logs the result
            - Returns the response
    """

    async def dispatch(self, request: Request, call_next):
        start_time = time.time()
        response = await call_next(request)
        duration = time.time() - start_time
        print(f"⏱ Request: {request.url.path} processed in {duration:.5f} seconds")
        return response


class LoggingMiddleware(BaseHTTPMiddleware):
    """
    Middleware to log request details.

    Logs:
        - HTTP method (GET, POST, etc.)
        - Request path (e.g., /hello)
        - Client IP address

    Helps in debugging, monitoring, and auditing requests.
    """

    async def dispatch(self, request: Request, call_next):
        client_host = request.client.host if request.client else "unknown"
        print(f"📄 Request received: {request.method} {request.url.path} from {client_host}")
        response = await call_next(request)
        return response


# Add custom middlewares to the FastAPI application
# Order matters: LoggingMiddleware → TimerMiddleware → Route Handler
app.add_middleware(LoggingMiddleware)
app.add_middleware(TimerMiddleware)


@app.get('/hello')
async def hello():
    """
    Sample endpoint to demonstrate middleware effects.

    This endpoint performs a dummy loop to simulate workload so 
    that execution time is noticeable when measured by TimerMiddleware.
    """
    for _ in range(1000000):
        pass  # simulate computation workload
    return {'message': "Hello World!"}
