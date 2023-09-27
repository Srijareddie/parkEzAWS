from sqlalchemy import create_engine
from app.database.database import Base
from app.database.Models import business
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get database details from environment variables
DATABASE_HOSTNAME = os.getenv("DATABASE_HOSTNAME")
DATABASE_PORT = os.getenv("DATABASE_PORT")
DATABASE_NAME = os.getenv("DATABASE_NAME")
DATABASE_USERNAME = os.getenv("DATABASE_USERNAME")
DATABASE_PASSWORD = os.getenv("DATABASE_PASSWORD")

# Construct the DATABASE_URL
DATABASE_URL = f"postgresql://{DATABASE_USERNAME}:{DATABASE_PASSWORD}@{DATABASE_HOSTNAME}:{DATABASE_PORT}/{DATABASE_NAME}"

engine = create_engine(DATABASE_URL)

with engine.begin() as connection:
    Base.metadata.drop_all(connection)
    Base.metadata.create_all(connection)