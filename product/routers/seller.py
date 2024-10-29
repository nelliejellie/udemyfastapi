from fastapi import APIRouter,status,Response,HTTPException
from .. import schemas
from .. import models
from .. database import engine,SessionLocal,get_db
from fastapi.params import Depends
from sqlalchemy.orm import Session
from sqlalchemy.sql.functions import mode
from typing import List
from passlib.context import CryptContext

router = APIRouter(tags=["Sellers"])

pwd_context = CryptContext(
      schemes=["bcrypt"],
      deprecated="auto",
    )


@router.post('/seller', response_model=schemas.DisplaySeller)
def create_seller(request:schemas.Seller,db: Session = Depends(get_db)):
    hashpassword = pwd_context.hash(request.password)
    new_seller = models.Seller(username=request.username, email=request.email,password=hashpassword)
    db.add(new_seller)
    db.commit()
    db.refresh(new_seller)
    return new_seller

@router.get('/sellers', response_model=List[schemas.DisplaySeller])
def sellers(db: Session = Depends(get_db)):
    sellers = db.query(models.Seller).all()
    return sellers