"""
FastAPI User Authentication Example
===================================

This file demonstrates a **basic authentication system** in FastAPI using
OAuth2 with password flow.

Key Features:
-------------
1. `/token` endpoint: Accepts username & password via form data and returns a fake access token.
2. `decode_token`: Simulates token validation by checking if the token is valid.
3. `get_current_user`: Dependency function that extracts and validates the token from requests.
4. `/profile` endpoint: A protected route that requires authentication.

Concept:
--------
- OAuth2PasswordBearer: FastAPI’s built-in class that extracts a bearer token from the `Authorization` header.
- Dependency Injection (`Depends`): Used to automatically pass the token into `get_current_user`.
- HTTPException: Raised when credentials are invalid.

Authentication Flow:
--------------------
1. Client sends POST request to `/token` with username and password (form fields).
2. If credentials are correct → returns `{"access_token": "valid_token", "token_type": "bearer"}`.
3. Client must include this token in subsequent requests:
       Authorization: Bearer valid_token
4. FastAPI uses `OAuth2PasswordBearer` to extract the token from the header.
5. `get_current_user` runs → calls `decode_token` → verifies token.
6. If valid → endpoint gets the decoded user object.
7. If invalid → raises `401 Unauthorized`.

NOTE: 
This is only a **demo**. In real-world apps:
    - Passwords should be hashed (not plain text).
    - Tokens should be JWTs (not hardcoded strings).
    - OAuth2 flows with refresh tokens should be implemented.

"""

from fastapi import FastAPI, Depends, Form, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

# Initialize FastAPI app
app = FastAPI()

# OAuth2PasswordBearer will read tokens from the "Authorization: Bearer <token>" header.
oauth2_scheme = OAuth2PasswordBearer(tokenUrl='token')


@app.post('/token')
def login(username: str = Form(...), password: str = Form(...)):
    """
    Login endpoint to authenticate a user.

    Args:
        username (str): The username from form data.
        password (str): The password from form data.

    Returns:
        dict: An access token if authentication succeeds.

    Logic:
        - If username is 'john' and password is 'pass123', return a fake token.
        - Otherwise, raise HTTP 400 (Bad Request) with 'Invalid Credentials'.
    """
    if username == 'john' and password == 'pass123':
        return {'access_token': 'valid_token', 'token_type': 'bearer'}

    # Invalid credentials → raise error
    raise HTTPException(status_code=400, detail='Invalid Credentials')


def decode_token(token: str):
    """
    Simulates decoding and validating an access token.

    Args:
        token (str): The bearer token extracted from the request.

    Returns:
        dict: A mock user dictionary if the token is valid.

    Logic:
        - If token equals 'valid_token', return a fake user (john).
        - Otherwise, raise HTTP 401 Unauthorized.
    """
    if token == 'valid_token':
        return {'name': 'john'}

    # Invalid token → raise 401 Unauthorized
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid Authentication Credentials"
    )


def get_current_user(token: str = Depends(oauth2_scheme)):
    """
    Dependency function to get the current authenticated user.

    Args:
        token (str): Automatically extracted bearer token from the request header.

    Returns:
        dict: The decoded user object.

    Logic:
        - Calls `decode_token` to verify token validity.
        - If valid → returns the user dictionary.
        - If invalid → raises 401 Unauthorized.
    """
    return decode_token(token)


@app.get('/profile')
def get_profile(user=Depends(get_current_user)):
    """
    Protected endpoint that requires authentication.

    Args:
        user (dict): The currently authenticated user (injected by `get_current_user`).

    Returns:
        dict: Profile information of the authenticated user.

    Logic:
        - If a valid token is provided → returns `{'username': user['name']}`.
        - If no/invalid token → request is rejected before reaching here.
    """
    return {'username': user['name']}
