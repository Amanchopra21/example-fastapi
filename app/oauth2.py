from jose import JWTError, jwt
from datetime import datetime , timedelta
from. import schemas , oauth2 , database , models
from fastapi import Depends , status , HTTPException
from fastapi.security.oauth2 import OAuth2PasswordBearer    
from sqlalchemy.orm import Session
from .config import settings
# secret key
# algorithm 
# expiration time 

SECRET_KEY = settings.secret_key
ALGORITHM = settings.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")  # login is path where user will send username and password to get token

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_access_token(toekn : str , credentials_exception):
    try:
        payload = jwt.decode(toekn, SECRET_KEY, algorithms=[ALGORITHM])
        id : str = payload.get("user_id")
        if id is None:
            raise credentials_exception
        token_data = schemas.TokenData(id=id) # we are creating object of TokenData schema and passing id to it and then returning that object because we will use that id to get user from db in get_current_user function below  
    except JWTError:
        raise credentials_exception
    return token_data

def get_current_user(token : str = Depends(oauth2_scheme), db : Session = Depends(database.get_db)):
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, 
                                          detail=f"Could not validate credentials", headers={"WWW-Authenticate": "Bearer"})
    token = verify_access_token(token, credentials_exception)

    user = db.query(models.User).filter(models.User.id == token.id).first()# token.id is id we got from token and we are using that id to get user from db and then returning that user
    return user  
    