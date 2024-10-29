from pydantic import BaseModel

class Product(BaseModel):
    name:str
    description:str
    price:str

class DisplayProduct(Product):
    # if you want this to be the response
    # description:str
    # price:str
    class Config:
        orm_mode = True