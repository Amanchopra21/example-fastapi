from fastapi import FastAPI , Response , status, HTTPException , Depends
from pydantic import BaseModel
from fastapi.params import Body
from random import randrange
from sqlalchemy.orm import Session
from . import models , schemas , utils
from .database import engine , get_db
from .router import posts , users , auth , vote
from .config import settings
from fastapi.middleware.cors import CORSMiddleware

# models.Base.metadata.create_all(bind=engine)     



# my_posts = [{"title":"title of post 1", "content":"content of post 1", "id": 1},
            
#             {"title":"title of post 2", "content":"content of post 2" , "id": 2}]

origins = ["*"] # this is used to allow all origins to access our api and * means all origins

app = FastAPI() # created insance of fastapi and FASTAPI is a class and app is an object of that class



app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


print(settings) 
# def find_post(id):
#     for p in my_posts:
#         if p['id'] == id:
#             return p

# def find_post_index(id):
#     for i,p in enumerate(my_posts):
#         if p['id'] == id:
#             return i


app.include_router(posts.router)
app.include_router(users.router)
app.include_router(auth.router) 
app.include_router(vote.router) 

@app.get("/")
async def root():
    return {"message": "Hello World"}





