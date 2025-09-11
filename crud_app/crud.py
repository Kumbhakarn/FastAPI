"""
crud.py

This module encapsulates all database operations for the Employee model.

Purpose:
    - Provides an abstraction layer between API routes and database logic.
    - Keeps CRUD operations modular, reusable, and easy to maintain.
"""

from sqlalchemy.orm import Session
from crud_app import models, schemas


def get_employees(db: Session):
    """
    Retrieve all employees from the database.

    Args:
        db (Session): SQLAlchemy session object.

    Returns:
        List[Employee]: List of all Employee objects.
    """
    return db.query(models.Employee).all()


def get_employee(db: Session, emp_id: int):
    """
    Retrieve a single employee by ID.

    Args:
        db (Session): SQLAlchemy session object.
        emp_id (int): ID of the employee to fetch.

    Returns:
        Employee | None: The employee object if found, else None.
    """
    return db.query(models.Employee).filter(models.Employee.id == emp_id).first()


def create_employee(db: Session, employee: schemas.EmployeeCreate):
    """
    Create a new employee record.

    Args:
        db (Session): SQLAlchemy session object.
        employee (EmployeeCreate): Pydantic schema with employee details.

    Returns:
        Employee: The newly created employee object.
    """
    db_employee = models.Employee(
        name=employee.name,
        email=employee.email
    )
    db.add(db_employee)
    db.commit()
    db.refresh(db_employee)
    return db_employee


def update_employee(db: Session, emp_id: int, employee: schemas.EmployeeUpdate):
    """
    Update an existing employee record.

    Args:
        db (Session): SQLAlchemy session object.
        emp_id (int): ID of the employee to update.
        employee (EmployeeUpdate): Pydantic schema with updated details.

    Returns:
        Employee | None: The updated employee object if found, else None.
    """
    db_employee = db.query(models.Employee).filter(models.Employee.id == emp_id).first()

    if db_employee:
        db_employee.name = employee.name
        db_employee.email = employee.email
        db.commit()
        db.refresh(db_employee)

    return db_employee


def delete_employee(db: Session, emp_id: int):
    """
    Delete an employee record by ID.

    Args:
        db (Session): SQLAlchemy session object.
        emp_id (int): ID of the employee to delete.

    Returns:
        Employee | None: The deleted employee object if found, else None.
    """
    db_employee = db.query(models.Employee).filter(models.Employee.id == emp_id).first()

    if db_employee:
        db.delete(db_employee)
        db.commit()

    return db_employee
