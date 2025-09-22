"""
schemas.py

This module defines the Pydantic models (schemas) used for request and response
validation in the CRUD application.

Schemas ensure that data exchanged via the API follows the correct format.
They also act as a contract between the backend and the client.
"""

from pydantic import BaseModel, EmailStr


class EmployeeBase(BaseModel):
    """
    Base schema for Employee with common fields.

    Attributes:
        name (str): Name of the employee.
        email (EmailStr): Valid email address of the employee.
    """
    name: str
    email: EmailStr


class EmployeeCreate(EmployeeBase):
    """
    Schema for creating a new Employee.
    Inherits all fields from EmployeeBase.
    """
    pass


class EmployeeUpdate(EmployeeBase):
    """
    Schema for updating an existing Employee.
    Inherits all fields from EmployeeBase.
    """
    pass


class EmployeeOut(EmployeeBase):
    """
    Schema for returning Employee data in API responses.

    Attributes:
        id (int): Unique identifier of the employee.
    """

    id: int

    class Config:
        orm_mode = True  # Allows compatibility with SQLAlchemy ORM objects
