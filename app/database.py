# DB connection and setup

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .schemas import Base

DATABASE_URL = "mysql+mysqlconnector://devuser:devpass@localhost:3306/mydb"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create tables
#Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)
