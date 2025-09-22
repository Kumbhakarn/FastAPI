"""
Integration Tests for FastAPI Application (test_main.py)
========================================================

Purpose:
--------
This file contains **integration tests** for the FastAPI application 
defined in `main.py`.  
It ensures that the `/loan_eligibility` endpoint behaves correctly under 
different scenarios.

Why Integration Testing?
------------------------
- Validates that the **API endpoints**, **dependencies**, and **business logic** 
  all work together as expected.
- Simulates real client-server interaction using FastAPI's `TestClient`.
- Ensures responses (status codes + JSON bodies) match expected behavior.

Testing Framework:
------------------
- Uses `pytest` style test functions.
- `TestClient` is provided by FastAPI (built on `requests`) to send test HTTP requests.

Endpoints Tested:
-----------------
- `POST /loan_eligibility`
    - Accepts a JSON payload with fields: `income`, `age`, `employment_status`.
    - Returns eligibility decision: `{'eligible': True/False}`.

Test Cases:
-----------
1. `test_eligibility_pass`:
   - Input: Higher income, valid age, employed.
   - Expected: Eligible → `{'eligible': True}` with HTTP 200.

2. `test_eligibility_fail`:
   - Input: Low income, young age, unemployed.
   - Expected: Not eligible → `{'eligible': False}` with HTTP 200.
"""

from fastapi.testclient import TestClient
from app.main import app
import pytest

# Create a test client for the FastAPI app
client = TestClient(app)


def test_eligibility_pass():
    """
    Test Case: Loan eligibility - PASS
    ----------------------------------
    Input:
        income: 60000
        age: 25
        employment_status: 'employed'

    Expectation:
        - API should return status code 200.
        - JSON response should indicate `eligible: True`.

    Logic:
        Since the applicant has high income and is employed,
        they should qualify as eligible.
    """
    payload = {
        'income': 60000,
        'age': 25,
        'employment_status': 'employed'
    }
    response = client.post('/loan_eligibility', json=payload)

    assert response.status_code == 200
    assert response.json() == {'eligible': True}


def test_eligibility_fail():
    """
    Test Case: Loan eligibility - FAIL
    ----------------------------------
    Input:
        income: 30000
        age: 18
        employment_status: 'unemployed'

    Expectation:
        - API should return status code 200.
        - JSON response should indicate `eligible: False`.

    Logic:
        Since the applicant has low income, is unemployed,
        and just at minimum age, they should be marked as ineligible.
    """
    payload = {
        'income': 30000,
        'age': 18,
        'employment_status': 'unemployed'
    }
    response = client.post('/loan_eligibility', json=payload)

    assert response.status_code == 200
    assert response.json() == {'eligible': False}

# ==========================================================
# Parameterized Tests for Income
# ==========================================================

@pytest.mark.parametrize("income, expected", [
    (10000, False),   # Too low income → Fail
    (40000, False),   # Borderline case → Fail
    (60000, True),    # Sufficient income → Pass
    (100000, True),   # High income → Pass
])

def test_income_cases(income, expected):
    payload = {'income': income, 'age': 30, 'employment_status': 'employed'}
    response = client.post('/loan_eligibility', json=payload)

    assert response.status_code == 200
    assert response.json() == {'eligible': expected}


# ==========================================================
# Parameterized Tests for Age
# ==========================================================

@pytest.mark.parametrize("age, expected", [
    (16, False),   # Too young → Fail
    (18, False),   # Minimum age but not sufficient → Fail
    (25, True),    # Young adult with valid age → Pass
    (60, True),    # Older but still eligible → Pass
])
def test_age_cases(age, expected):
    payload = {'income': 70000, 'age': age, 'employment_status': 'employed'}
    response = client.post('/loan_eligibility', json=payload)

    assert response.status_code == 200
    assert response.json() == {'eligible': expected}


# ==========================================================
# Parameterized Tests for Employment Status
# ==========================================================

@pytest.mark.parametrize("status, expected", [
    ('unemployed', False),  # No job → Fail
    ('student', False),     # Still studying → Fail
    ('employed', True),     # Full-time job → Pass
    ('self-employed', True) # Business/self-employed → Pass
])
def test_employment_status_cases(status, expected):
    payload = {'income': 80000, 'age': 28, 'employment_status': status}
    response = client.post('/loan_eligibility', json=payload)

    assert response.status_code == 200
    assert response.json() == {'eligible': expected}