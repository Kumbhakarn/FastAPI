from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

                        # "database_name:///./test.db" (/.= current Directory)  (/test.db = file name)
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db" # giving database url 

# Create_engine = makes a connection with database
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={'check_same_thred':False}
    )

SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)
# sessionmaker = makes new session to do our work 
# each session repreasent a transaction 
# autoflush = False : SQLAlchemany will not automatically flush the changes.
# we have to commit for changes manually

Base = declarative_base()
# creates a base class for models to inherit from linking the python classes with the tables