"""
Main Application File (main.py)
===============================

This is the entry point of the FastAPI application.  
It integrates authentication logic (JWT, password hashing, user retrieval)  
and exposes API endpoints for **login** and **protected user data**.

Purpose:
--------
- Authenticate users via OAuth2 (username + password).
- Generate JWT access tokens for logged-in users.
- Validate tokens for secure access to protected routes.

Modules Used:
-------------
- FastAPI: Web framework for building APIs.
- OAuth2PasswordBearer & OAuth2PasswordRequestForm: 
  Utilities for implementing OAuth2 login flow.
- jwt_authentication.auth: Handles JWT token creation & validation.
- jwt_authentication.utils: Contains helper functions for user data and password verification.

Constants:
----------
- `oath2_scheme`: Dependency that extracts bearer tokens from requests.
"""

from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

# Import custom authentication utilities
from jwt_authentication.auth import create_access_tokens, verify_token
from jwt_authentication.utils import get_user, verify_password


# ==========================================================
# Application Setup
# ==========================================================
app = FastAPI()

# Dependency for OAuth2: looks for "Authorization: Bearer <token>" header
oath2_scheme = OAuth2PasswordBearer(tokenUrl='token')


# ==========================================================
# Endpoints
# ==========================================================

@app.post('/token')
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    """
    Login endpoint (POST /token)
    ----------------------------
    Purpose:
        Authenticate user credentials and generate an access token.

    Args:
        form_data (OAuth2PasswordRequestForm): 
            Automatically extracted login form with `username` and `password`.

    Returns:
        dict: 
            - access_token: JWT token for the session.
            - token_type: Authentication scheme ("bearer").

    Logic:
        1. Retrieve user from the mock database (`get_user`).
        2. If user not found → raise HTTP 400 (Invalid Username).
        3. Verify password against stored hash (`verify_password`).
           - If mismatch → raise HTTP 400 (Invalid Password).
        4. If valid → create JWT (`create_access_tokens`) with username as subject (`sub`).
        5. Return token and token type.
    """
    user_dict = get_user(form_data.username)
    if not user_dict:
        raise HTTPException(status_code=400, detail="Invalid User Name")

    if not verify_password(form_data.password, user_dict['hashed_password']):
        raise HTTPException(status_code=400, detail="Invalid Password")

    access_token = create_access_tokens(data={'sub': form_data.username})
    return {'access_token': access_token, 'token_type': 'bearer'}


@app.get('/users')
def read_users(token: str = Depends(oath2_scheme)):
    """
    Protected Endpoint (GET /users)
    -------------------------------
    Purpose:
        Validate the provided JWT token and return user information.

    Args:
        token (str): Extracted automatically from "Authorization: Bearer <token>" header.

    Returns:
        dict:
            - username: The username extracted from the verified token.

    Logic:
        1. Extract token using `oath2_scheme` dependency.
        2. Verify token using `verify_token`.
           - If invalid/expired → raise HTTP 401 Unauthorized.
        3. Extract and return `username` claim from token.
    """
    username = verify_token(token)
    return {'username': username}
