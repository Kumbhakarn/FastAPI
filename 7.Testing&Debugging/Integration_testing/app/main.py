"""
Main Application File (main.py)
===============================

Purpose:
--------
This file defines the main FastAPI application for loan eligibility checks.  

It provides:
- A **Pydantic model** (`Applicant`) for request validation.
- An endpoint `/loan_eligibility` that accepts applicant details.
- A call to the **business logic function** (`is_eligable_for_load`) to determine eligibility.

Integration with logic.py:
--------------------------
- `main.py` focuses on **API definition** (inputs/outputs).
- `logic.py` contains the **business rules** for determining eligibility.
- This separation makes the code modular, testable, and maintainable.

Flow of a Request:
------------------
1. A client sends a POST request to `/loan_eligibility` with a JSON body.
2. FastAPI automatically validates the input against the `Applicant` model:
   - `income` (float)
   - `age` (int)
   - `employment_status` (str)
3. The validated data is passed into the `is_eligable_for_load` function.
4. The function applies business rules and returns a boolean (True/False).
5. The endpoint returns a JSON response: `{"eligible": <bool>}`.

Why Pydantic?
-------------
- Ensures that request data has the correct types.
- Rejects invalid or malformed requests before hitting business logic.
- Provides automatic API documentation in Swagger UI.

"""

from fastapi import FastAPI
from pydantic import BaseModel
from app.logic import is_eligable_for_load


# ==========================================================
# Application Setup
# ==========================================================
app = FastAPI()


# ==========================================================
# Data Model
# ==========================================================
class Applicant(BaseModel):
    """
    Pydantic model representing a loan applicant.

    Attributes:
        income (float): Monthly or annual income of the applicant.
        age (int): Applicant's age (must meet minimum requirement).
        employment_status (str): Employment type (e.g., "employed", "self-employed", "unemployed").

    Purpose:
        - Validates incoming request data.
        - Prevents incorrect types (e.g., string instead of number).
    """
    income: float
    age: int
    employment_status: str 


# ==========================================================
# Endpoints
# ==========================================================
@app.post('/loan_eligibility')
def check_eligibility(applicant: Applicant):
    """
    Loan Eligibility Endpoint
    -------------------------
    Path: /loan_eligibility  
    Method: POST  

    Request Body:
        Applicant model containing:
            - income (float)
            - age (int)
            - employment_status (str)

    Response:
        JSON object:
            {"eligible": bool}

    Logic:
        1. Extract applicant data from request (validated by Pydantic).
        2. Call `is_eligable_for_load` from logic.py with applicant details.
        3. Return whether the applicant is eligible as a JSON response.

    Example:
    --------
    Request:
        POST /loan_eligibility
        {
            "income": 60000,
            "age": 25,
            "employment_status": "employed"
        }

    Response:
        {
            "eligible": true
        }
    """
    eligibility = is_eligable_for_load(
        income=applicant.income,
        age=applicant.age,
        employment_status=applicant.employment_status
    )

    return {"eligible": eligibility}