#  BUILDING THE DATABASE MODEL:

from sqlalchemy.ext.declarative import declarative_base # importing the base model
from sqlalchemy import Column,Integer,String,Float # importing the columns and defining their types.

Base = declarative_base()

class Product(Base): # inheriting the declarative_base module.
    __tablename__ = "product" # defining the table name.
    
    id = Column(Integer,primary_key=True,index=True) # creating a primary key.
    name = Column(String)
    description = Column(String)
    price = Column(Float)
    quantity = Column(Integer)