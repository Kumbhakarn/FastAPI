"""
Utility Functions for Authentication
====================================

This module contains **helper functions and constants** that make the authentication
system more modular and reusable. It focuses on **password hashing/verification** and
retrieving users from a mock database.

Purpose:
--------
- Centralizes common logic (e.g., password handling) so it can be reused across files.
- Improves maintainability by keeping utility functions separate from routes.
- Keeps authentication secure by properly handling password hashing and validation.

Libraries Used:
---------------
- `passlib`: A password hashing library that supports modern secure algorithms (e.g., bcrypt).
- `CryptContext`: A Passlib class that simplifies password hashing and verification by
  managing algorithms and deprecation policies.

Components:
-----------
1. `pwd_context`: Cryptographic context with bcrypt hashing algorithm.
2. `fake_user_db`: A simulated database with one pre-registered user.
3. `get_user(username)`: Retrieves user information from the fake database.
4. `verify_password(plain_password, hashed_password)`: Verifies a plain password against its hash.

Note:
-----
- In real-world projects, `fake_user_db` should be replaced with an actual database.
- Passwords must **always** be stored in hashed form (never plain text).
- Bcrypt is a recommended algorithm due to its security and resistance to brute-force attacks.

"""

from passlib.context import CryptContext

# ==========================================================
# Cryptographic Context
# ==========================================================
# Configure Passlib's CryptContext with bcrypt algorithm.
# `deprecated='auto'` ensures old algorithms are migrated automatically.
pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')


# ==========================================================
# Mock User Database (for demo purposes only)
# ==========================================================
fake_user_db = {
    'johndoe': {
        'username': 'johndoe',
        # Store only hashed passwords, never plain-text ones
        'hashed_password': pwd_context.hash('secret123')
    }
}


# ==========================================================
# Utility Functions
# ==========================================================

def get_user(username: str) -> dict | None:
    """
    Retrieve a user record from the fake database.

    Args:
        username (str): The username to look up.

    Returns:
        dict | None: The user dictionary if found, otherwise None.

    Logic:
        - Looks up `username` in `fake_user_db`.
        - If user exists → return dictionary with user details.
        - If not found → return None.
    """
    user = fake_user_db.get(username)
    return user


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify a plain-text password against its hashed counterpart.

    Args:
        plain_password (str): The raw password entered by the user.
        hashed_password (str): The stored hashed password from the database.

    Returns:
        bool: True if the password matches, False otherwise.

    Logic:
        - Uses `pwd_context.verify` to safely compare plain and hashed password.
        - Prevents direct string comparison (which is insecure).
    """
    return pwd_context.verify(plain_password, hashed_password)
