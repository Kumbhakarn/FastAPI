"""
main.py

This is where the FastAPI application is defined.
It exposes API endpoints to perform CRUD operations on Employee records.

Endpoints:
    - POST   /employees        → Create a new employee
    - GET    /employees        → Retrieve all employees
    - GET    /employees/{id}   → Retrieve a specific employee
    - PUT    /employees/{id}   → Update an existing employee
    - DELETE /employees/{id}   → Delete an employee
"""

from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from crud_app.database import engine, SessionLocal, Base
from typing import List
from crud_app import models, schemas, crud

# Create the database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Employee CRUD API", version="1.0")


# Dependency to get DB session
def get_db():
    """
    Dependency that provides a database session.
    Ensures session is closed after the request lifecycle.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# 1. Create an Employee
@app.post('/employees', response_model=schemas.EmployeeOut)
def create_employee(employee: schemas.EmployeeCreate, db: Session = Depends(get_db)):
    """
    Create a new employee record.

    Args:
        employee (EmployeeCreate): Data for the new employee.
        db (Session): SQLAlchemy session (injected by dependency).

    Returns:
        EmployeeOut: The newly created employee.
    """
    return crud.create_employee(db, employee)


# 2. Get all Employees
@app.get('/employees', response_model=List[schemas.EmployeeOut])
def get_employees(db: Session = Depends(get_db)):
    """
    Retrieve all employees from the database.
    """
    return crud.get_employees(db)


# 3. Get specific Employee
@app.get('/employees/{emp_id}', response_model=schemas.EmployeeOut)
def get_employee(emp_id: int, db: Session = Depends(get_db)):
    """
    Retrieve an employee by ID.

    Args:
        emp_id (int): Employee ID.

    Raises:
        HTTPException: If employee is not found.

    Returns:
        EmployeeOut: The employee object.
    """
    employee = crud.get_employee(db, emp_id)
    if employee is None:
        raise HTTPException(status_code=404, detail="Employee Not Found")
    return employee


# 4. Update an Employee
@app.put('/employees/{emp_id}', response_model=schemas.EmployeeOut)
def update_employee(emp_id: int, employee: schemas.EmployeeUpdate, db: Session = Depends(get_db)):
    """
    Update an existing employee by ID.

    Args:
        emp_id (int): Employee ID.
        employee (EmployeeUpdate): Updated employee details.

    Raises:
        HTTPException: If employee is not found.

    Returns:
        EmployeeOut: The updated employee object.
    """
    db_employee = crud.update_employee(db, emp_id, employee)
    if db_employee is None:
        raise HTTPException(status_code=404, detail="Employee Not Found")
    return db_employee


# 5. Delete an Employee
@app.delete('/employees/{emp_id}', response_model=dict)
def delete_employee(emp_id: int, db: Session = Depends(get_db)):
    """
    Delete an employee by ID.

    Args:
        emp_id (int): Employee ID.

    Raises:
        HTTPException: If employee is not found.

    Returns:
        dict: Confirmation message.
    """
    employee = crud.delete_employee(db, emp_id)
    if employee is None:
        raise HTTPException(status_code=404, detail="Employee Not Found")
    return {"detail": "Employee Deleted"}
