"""
models.py

This module defines the ORM (Object Relational Mapping) classes for the CRUD application.  
Each class corresponds to a database table, allowing Python objects to map directly  
to relational database rows.

In this example:
- The `Employee` class maps to the `employees` table.
- Each class attribute represents a column in the table.
"""

from sqlalchemy import Column, Integer, String
from crud_app.database import Base


class Employee(Base):
    """
    ORM model representing an Employee in the database.

    Table Name:
        employees

    Columns:
        id (int): Primary key, auto-generated ID for each employee.
        name (str): Name of the employee. Indexed for faster lookups. Cannot be null.
        email (str): Unique email address of the employee. Indexed and must be unique.
    """

    __tablename__ = "employees"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
