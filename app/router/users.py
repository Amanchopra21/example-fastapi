from fastapi import Response , status, HTTPException , Depends , APIRouter
from .. import models , schemas , utils
from .. database import get_db
from sqlalchemy.orm import Session

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)

@router.post("/",status_code=status.HTTP_201_CREATED,response_model=schemas.UserResponse)
def create_user(user : schemas.UserCreate, db:Session = Depends(get_db)):

    hashed_password = utils.hash(user.password) #user = object of UserCreate schema(pydantic model) 
    user.password = hashed_password
    new_user = models.User(**user.dict()) # User is sql table and models.User is sqlalchemy model
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user

@router.get("/{id}",response_model=schemas.UserResponse)
def get_user(id : int , db:Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()   #model.User is sqlalchemy model User is sql table   
    if not user:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail=f"user with id: {id} was not found")
    return user