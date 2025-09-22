"""
Pydantic Data Models for FastAPI
================================

This file defines **Pydantic models** that are used for:
- Validating request data (e.g., login forms, user creation).
- Structuring response data.
- Defining how data is represented internally (e.g., user in DB vs. user input).

Why Pydantic Models?
--------------------
- FastAPI relies on Pydantic for automatic data validation.
- Ensures type safety (e.g., `username: str` must be a string).
- Converts input/output data into well-defined Python objects.
- Provides clear API documentation (via OpenAPI/Swagger).

Models Defined:
---------------
1. `User`:
   - Represents a **basic user object** (username + password).
   - Used for user input (e.g., login request payload).

2. `UserInDB`:
   - Inherits from `User`.
   - Adds an extra field `hashed_password`.
   - Represents how the user is stored in the database (never store raw password).

Flow:
-----
- Client sends request → FastAPI validates against `User`.
- Server transforms `User.password` into `UserInDB.hashed_password` before saving to DB.
- Responses may exclude sensitive fields (like `hashed_password`) to protect user data.

"""

from pydantic import BaseModel


class User(BaseModel):
    """
    Base user model used for input validation.

    Attributes:
        username (str): The username of the user.
        password (str): The plain-text password (only used for login/registration input).

    Purpose:
        - Used when accepting user credentials from clients (e.g., login form).
        - Ensures both `username` and `password` are strings and required.
    """
    username: str
    password: str


class UserInDB(User):
    """
    User model representing how users are stored in the database.

    Inherits:
        User: Includes `username` and `password`.

    Additional Attributes:
        hashed_password (str): The password stored securely in hashed form.

    Purpose:
        - Represents users in persistence/storage layer.
        - Prevents storing plain-text passwords (always store hashed versions).
        - Bridges the gap between user input (`User`) and database records.
    """
    hashed_password: str
