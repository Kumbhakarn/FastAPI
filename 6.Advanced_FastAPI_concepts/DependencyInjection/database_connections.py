"""
FastAPI Dependency Injection Example
====================================

This file demonstrates **Dependency Injection (DI)** in FastAPI using the `Depends` utility.

Why Dependency Injection?
-------------------------
- Keeps your code **modular and reusable**.
- Helps you **separate concerns** (e.g., database logic vs. business logic).
- Makes it easier to **test components independently**.
- Reduces **code duplication**.

Concept:
--------
- `Depends` is used in FastAPI to declare dependencies for routes.
- A dependency can be a function, class, or generator.
- Dependencies can be reused across multiple endpoints.

Here, we simulate a database connection using a dependency function `get_db`.
The endpoint `/home` depends on this "database connection".

Flow:
-----
1. Client sends a request to `/home`.
2. FastAPI sees `db=Depends(get_db)` and executes `get_db()`.
3. `get_db` yields a mock database connection.
4. The endpoint receives this connection as the `db` parameter.
5. The endpoint uses it to return the database status.
6. Once the request is done, FastAPI executes the `finally` block in `get_db`
   to "close" the connection (cleanup).

"""

from fastapi import FastAPI, Depends

# Initialize FastAPI app
app = FastAPI()


# Dependency Function
def get_db():
    """
    Dependency function that simulates a database connection.

    Returns:
        dict: A mock database connection object.

    Usage:
        - Called automatically by FastAPI when an endpoint has `db=Depends(get_db)`.
        - Uses a generator pattern (`yield`) so cleanup logic can be executed after the request.
    """
    db = {'connection': 'mock_db_connection'}  # simulate database connection

    try:
        # Yield the connection so the endpoint can use it
        yield db
    finally:
        # Cleanup code (executed after request is finished)
        # In real-world usage, you would call db.close() or session.close()
        print("Closing DB connection (simulated)")
        # db.close()  # (not applicable here since `db` is just a dict)


# Endpoint Example
@app.get('/home')
def home(db=Depends(get_db)):
    """
    Home endpoint that uses dependency injection to access the database.

    Args:
        db (dict): Injected dependency representing a database connection.

    Returns:
        dict: The status of the database connection.
    """
    return {'db_status': db['connection']}
