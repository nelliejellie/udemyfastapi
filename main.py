from fastapi import FastAPI
from pydantic import BaseModel, Field,HttpUrl
from typing import List,Set
from uuid import UUID
from datetime import date, datetime,time,timedelta


class Event(BaseModel):
    event_id:UUID
    start_date:date
    start_time:datetime
    end_time:datetime
    repeat_time:time
    execute_after: timedelta

    
class Image(BaseModel):
    url: HttpUrl
    name: str

class Product(BaseModel):
    name: str = Field(examples="phone ")
    price:int = Field(title="price of the item",description="prcie",gt=0)
    discount:int
    discounted_price:float
    tags: Set[str] = []
    image: Image

    #defining an example schema
    class Config:
        schema_extra={
            "example":{
            "name":"phone",
            "price":100,
            "discount":10,
            "discount_price":0,
            "tags":["Electronics","computers"],
            "image":[
                {"url":"http://www.google.com","name":"phone_image"}
            ]
        }
        }

class Offer(BaseModel):
    name:str
    description:str
    price: float
    products:List[Product]

class Profile(BaseModel):
    name: str
    email: str 
    age:int
    image:List[Image]

app = FastAPI()

@app.post('/addproduct')
def addproduct(product:Product):
    product.discounted_price = product.price - (product.price * product.discount)/100
    return product

@app.post('/addUser')
def adduser(profile:Profile):
    return profile

@app.post('/addoffer')
def addOffer(offer:Offer):
    return offer