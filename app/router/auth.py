from fastapi import APIRouter , Depends , HTTPException , status , Response
from  fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from ..database import get_db 
from ..import schemas , models , utils , oauth2
router = APIRouter(
    tags=["Authentication"]
)

@router.post("/login" , response_model=schemas.Token)


# def login(user_credentials : schemas.Userlogin,db:Session = Depends(get_db)):

def login(user_credentials : OAuth2PasswordRequestForm = Depends(),db:Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == user_credentials.username).first() #user_credentials.username is email 
    if not user:
        raise HTTPException(status_code = status.HTTP_403_FORBIDDEN,detail = f"Invalid Credentials")
    
    if not utils.verify_password(user_credentials.password , user.password): #user.password is hashed password stored
    #in db and user is object of models.User and models.User is sqlalchemy model and table name is User
        raise HTTPException(status_code = status.HTTP_403_FORBIDDEN, detail = f"Invalid Credentials")
    
    #create a token and return
    access_token = oauth2.create_access_token(data={"user_id": user.id})
    return {"access_token": access_token,"token_type":"bearer"}