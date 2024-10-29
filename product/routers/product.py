from fastapi import APIRouter,status,Response,HTTPException
from .. import schemas
from .. import models
from .. database import engine,SessionLocal,get_db
from fastapi.params import Depends
from sqlalchemy.orm import Session
from sqlalchemy.sql.functions import mode
from typing import List
from passlib.context import CryptContext

router = APIRouter()

@router.post('/product',status_code=status.HTTP_201_CREATED,tags=["Products"])
def add(request: schemas.Product, db: Session = Depends(get_db)):
    new_product = models.Product(name=request.name, description=request.description, price=request.price,seller_id=1)
    db.add(new_product)
    db.commit()
    db.refresh(new_product)
    return request

@router.put('/product/{id}', response_model=schemas.DisplayProduct,tags=["Products"])
def update(id,response:Response, request:schemas.Product,db: Session = Depends(get_db)):
    product = db.query(models.Product).filter(models.Product.id == id) 
    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail='product not found')
    product.update(request.dict())
    db.commit()
    return {'product successfully updated'}

@router.get('/products', response_model=List[schemas.DisplayProduct],tags=["Products"])
def products(db: Session = Depends(get_db)):
    products = db.query(models.Product).all()
    return products

@router.get('/product/{id}',tags=["Products"])
def product(id,db: Session = Depends(get_db)):
    product = db.query(models.Product).filter(models.Product.id == id).first()
    return product

@router.delete('/product/{id}',tags=["Products"])
def delete(id,db: Session = Depends(get_db)):
    db.query(models.Product).filter(models.Product.id == id).delete(synchronize_session=False)
    db.commit()
    return {"product deleted"}