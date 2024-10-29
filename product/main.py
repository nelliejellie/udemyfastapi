from fastapi import FastAPI,status,Response,HTTPException
from . import schemas
from . import models
from . database import engine,SessionLocal,get_db
from . routers import product,seller


app = FastAPI(title="Products Api",description="get info for products",terms_of_service="",
      contact={
          "Developer Name":"Emeka Ewelike",
          "Email":"Emeka Ewelike"
      },
      license_info={
        "name":"blah",

      },
      docs_url="/docs"
      )
app.include_router(product.router)
app.include_router(seller.router)
models.Base.metadata.create_all(engine)






