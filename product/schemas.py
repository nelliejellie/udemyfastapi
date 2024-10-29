from pydantic import BaseModel

class Product(BaseModel):
    name:str
    description:str
    price:int

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

