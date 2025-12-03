# DATABASE CONNECTION
from sqlalchemy.engine import create_engine # importing the engine module.
from sqlalchemy.orm import sessionmaker # importing the sqlalchemy and session maker.

# CREATING A DATABASE URL:
db_url = "postgresql://postgres:YOUR_PASSWORD_HERE@localhost:5432/telusko"

# ENGINE MEANS THE DATABASE
engine= create_engine(db_url)

session = sessionmaker(autoflush=False,autocommit=False,bind=engine)