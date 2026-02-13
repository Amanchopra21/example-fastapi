from operator import le
from pydantic import BaseModel , EmailStr
from pydantic.types import conint
from datetime import datetime
from typing import Optional

class PostBase(BaseModel):    # user sending data to us [ means request body ]
    title:str
    content:str
    published : bool = True

class UserResponse(BaseModel):  # we are sending data to user
    id : int
    email : EmailStr
    created_at : datetime

    class Config:
        orm_mode = True

class PostCreate(PostBase):
    pass

class PostResponse(PostBase):   # we are sending data to user [ means response body ]
    id : int
    created_at : datetime 
    owner_id : int
    owner : UserResponse
    

    class Config:
        orm_mode = True

class PostOut(BaseModel):
    Post : PostResponse 
    votes : int

    class Config:
        orm_mode = True


class UserCreate(BaseModel):  # user sending data to us
    email : EmailStr
    password : str



class Userlogin(BaseModel): # user sending data to us
    email : EmailStr
    password : str

class Token(BaseModel):
    access_token : str
    token_type : str

class TokenData(BaseModel):
    id : Optional[int] = None

class Vote(BaseModel):
    post_id : int
    dir : conint(le=1) # conint is used to validate that dir should be either 0 or 1 and le is used to specify that dir should be less than or equal to 1