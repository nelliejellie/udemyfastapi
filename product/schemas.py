from pydantic import BaseModel
from typing import Optional

# request example
class Product(BaseModel):
    name:str
    description:str
    price:int

# response example
class DisplaySeller(BaseModel):
    username:str
    email:str

    class Config:
        orm_mode = True

class DisplayProduct(BaseModel):
    # if you want this to be the response
    description:str
    price:int
    seller: DisplaySeller
    class Config:
        orm_mode = True

class Seller(BaseModel):
    username:str
    email: str
    password:str

class Login(BaseModel):
    username:str
    password:str

class Token(BaseModel):
    access_token: str
    token_type:str

class TokenData(BaseModel):
    username: Optional[str] = None
