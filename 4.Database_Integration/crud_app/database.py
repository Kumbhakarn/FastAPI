"""
database.py

This module handles the database configuration and setup for the CRUD application.

Components:
    - SQLALCHEMY_DATABASE_URL: The connection string for the database (SQLite in this case).
    - engine: Creates a connection to the database using SQLAlchemy.
    - SessionLocal: A session factory for creating individual database sessions.
    - Base: A declarative base class used to define ORM models.

Usage:
    Import `SessionLocal` to create database sessions inside your routes or services.
    Import `Base` in your models module and extend it when defining ORM classes.
"""

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Database URL (using SQLite here, file stored as test.db in current directory)
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

# Engine: Core interface to the database
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

# SessionLocal: Factory for creating new session objects (transactions)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base: Used as a base class for ORM models (tables are created from these classes)
Base = declarative_base()
