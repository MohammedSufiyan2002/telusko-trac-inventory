from fastapi import Depends,FastAPI # importing fastapi and the "depends" module for dependency injection
from models import Product # importing the class Product
from database import session,engine # importing the session and engine module
import database_models # importing the database models.
from sqlalchemy.orm import Session 
from fastapi.middleware.cors import CORSMiddleware


myapp = FastAPI()

myapp.add_middleware(
    CORSMiddleware,
    allow_origins = ["http://localhost:3000"],
    allow_methods = ["*"]
)

database_models.Base.metadata.create_all(bind=engine)

@myapp.get("/") # "/" THIS IS MEANS IT IS REFERRING TO THE HOME PAGE
def greet():
    return "Welcome to TELUSKO TRAC!!!"

products = [
    Product(id=1,name="box",description="sweet box",price=75.5,quantity=3),
    Product(id=2,name="phone",description="redmi phone",price=7500.5,quantity=1),
    Product(id=3,name="plate",description="silver plates",price=50,quantity=5),
    Product(id=4,name="toy",description="batman toy",price=123.54,quantity=3),
]

def get_db(): # this function will automatically open and close the DB irrespective of the changes occur in DB or not.
    db = session() 
    try:
        yield db
    finally:
        db.close()


def init_db():
    db=session()
    count = db.query(database_models.Product).count # here, we are telling the DB to only do these steps if the Table is empty.
    if count == 0:
        for product in products:
            db.add(database_models.Product(**product.model_dump())) # separating the data into key-value pairs.
        
    db.commit() # this should be instantiated bcoz "autocommit" is in false mode.

init_db()

@myapp.get("/products") # ALSO "/" REFERS TO THE URL OF THE PAGE.
def get_all_products(db:Session = Depends(get_db)):
    db_products = db.query(database_models.Product).all()
    
    return db_products

@myapp.get("/products/{id}")
def get_product_by_id(id:int,db:Session = Depends(get_db)):
    db_product = db.query(database_models.Product).filter(database_models.Product.id==id).first()
    if db_product:
        return db_product    
    return "Product Not Found!"

@myapp.post("/products")
def adding_products(product:Product,db:Session = Depends(get_db)):
    db.add(database_models.Product(**product.model_dump()))
    db.commit()
    return product

@myapp.put("/products/{id}")
def update_products(id:int,product: Product,db:Session = Depends(get_db)):
    db_product = db.query(database_models.Product).filter(database_models.Product.id==id).first()
    if db_product:
        db_product.name = product.name
        db_product.description = product.description
        db_product.price = product.price
        db_product.quantity = product.quantity
        db.commit()
        return "Product Updated Successfully!!!"
    else:
        return "Product could not be added!"
            
@myapp.delete("/products/{id}")
def deleting_product(id:int,db:Session = Depends(get_db)):
    db_product = db.query(database_models.Product).filter(database_models.Product.id==id).first()
    if db_product:
        db.delete(db_product)
        db.commit()
        return "This Product has been Deleted!!!"
    else:
        return "Could not Find the Product!"
