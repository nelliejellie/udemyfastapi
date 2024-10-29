from fastapi import APIRouter,Depends,status,HTTPException
from ..import schemas,database,models
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from ..database import get_db
from datetime import datetime,timedelta
from jose import jwt,JWTError
from fastapi.security import OAuth2PasswordBearer,OAuth2PasswordRequestForm
from .. schemas import TokenData

SECRET_KEY = "test123abc"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 20

router = APIRouter(tags=["Auth"])

pwd_context = CryptContext(
      schemes=["bcrypt"],
      deprecated="auto",
    )
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth")
def generate_token(data:dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp":expire})
    encoded_jwt = jwt.encode(to_encode,SECRET_KEY,algorithm=ALGORITHM)
    return encoded_jwt


@router.post('/login')
def login(request:OAuth2PasswordRequestForm=Depends(), db: Session=Depends(get_db)):
    user = db.query(models.Seller).filter(models.Seller.username == request.username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)
    
    if not pwd_context.verify(request.password,user.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail='invalid password')
    
    access_token = generate_token(data={"sub":user.username})
    return {"access_token": access_token, "token_type":"bearer"}

def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid auth credentials",
        headers={'WWW-Authenticate':"Bearer"}
    )
    try:
        payload = jwt.decode(token,SECRET_KEY,algorithms=[ALGORITHM])
        username: str = payload.get('sub')
        if username is None:
            raise credentials_exception
            pass
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception