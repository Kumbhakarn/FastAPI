"""
JWT Authentication Utilities for FastAPI
========================================

This file provides helper functions and constants to handle **JWT (JSON Web Token) authentication**.

Purpose:
--------
- To securely authenticate users after login by generating JWTs.
- To verify tokens in subsequent requests to ensure the user is valid.
- To centralize all JWT-related logic so it can be reused across endpoints.

Concepts:
---------
- JWT (JSON Web Token) is a compact, secure way of transmitting user data between
  the server and client.
- Tokens consist of 3 parts: `header.payload.signature`.
- Common JWT claims include:
    - `sub`: Subject (usually the username or user ID).
    - `exp`: Expiration time (prevents infinite use of token).
- On login:
    - Server creates and signs a JWT with a secret key.
    - Client stores this token (e.g., in local storage or cookies).
    - For protected endpoints, client sends token in `Authorization: Bearer <token>` header.
    - Server verifies token on every request.

Constants:
----------
- `SECRET_KEY`: A secret string used to sign JWTs (must be kept safe!).
- `ALGORITHM`: The hashing algorithm used for signing tokens (HS256 in this case).
- `ACCESS_TOKEN_EXPIRY_MINUTES`: Expiration duration of the access token (default: 30 minutes).

Functions:
----------
1. `create_access_tokens(data: dict)`:
   - Creates a JWT access token for a given user payload.
   - Includes an expiration timestamp.
   - Returns the signed token string.

2. `verify_token(token: str)`:
   - Verifies and decodes a given JWT.
   - Validates expiration and claims.
   - Returns the username (`sub`) if valid.
   - Raises `HTTPException(401)` if invalid.

"""

from datetime import datetime, timedelta, timezone
from authlib.jose import JoseError, jwt
from fastapi import HTTPException


# =======================
# Constants
# =======================

# Secret key used for signing JWTs (keep this safe and never expose publicly).
SECRET_KEY = 'my_secrete'

# Algorithm used to sign JWTs (HMAC SHA-256).
ALGORITHM = 'HS256'

# Duration (in minutes) for which the access token is valid.
ACCESS_TOKEN_EXPIRY_MINUTES = 30


# =======================
# Functions
# =======================

def create_access_tokens(data: dict) -> str:
    """
    Create a JWT access token.

    Args:
        data (dict): Payload data to include in the token (e.g., {"sub": "username"}).

    Returns:
        str: Encoded JWT token as a string.

    Logic:
        - Define JWT header with chosen algorithm.
        - Calculate expiration timestamp (current UTC time + expiry minutes).
        - Add `exp` claim (expiration) to payload.
        - Encode the token using SECRET_KEY and return as a string.
    """
    header = {'alg': ALGORITHM}
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRY_MINUTES)

    payload = data.copy()  # copy input data so original isn't mutated
    payload.update({'exp': expire})  # add expiration claim

    # Encode header, payload, and secret key into a signed JWT
    return jwt.encode(header, payload, SECRET_KEY).decode('utf-8')


def verify_token(token: str) -> str:
    """
    Verify and decode a JWT access token.

    Args:
        token (str): The JWT token string to verify.

    Returns:
        str: The username (`sub` claim) if the token is valid.

    Raises:
        HTTPException 401: If the token is invalid, expired, or missing claims.

    Logic:
        - Decode the token using the SECRET_KEY.
        - Validate claims (expiration, etc.).
        - Extract the `sub` claim (username).
        - If missing or invalid → raise Unauthorized (401).
    """
    try:
        # Decode token with the secret key
        claims = jwt.decode(token, SECRET_KEY)

        # Validate built-in claims (e.g., expiration)
        claims.validate()

        # Extract username (subject)
        username = claims.get('sub')
        if username is None:
            raise HTTPException(status_code=401, detail='Token Missing')

        return username

    except JoseError:
        # Raised when token signature is invalid or expired
        raise HTTPException(status_code=401, detail="Couldn't validate Credentials")