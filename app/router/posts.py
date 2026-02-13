from fastapi import APIRouter, Response , status, HTTPException , Depends
from .. import models , schemas , oauth2
from .. database import get_db
from sqlalchemy.orm import Session
from typing import Optional, List
from sqlalchemy import func 



router = APIRouter(
    prefix="/posts",
    tags=["Posts"]
)


@router.get("/",response_model = List[schemas.PostOut])
def get_posts(db: Session = Depends(get_db),current_user: int = Depends(oauth2.get_current_user),
              limit : int = 10, skip :int = 0,search : Optional[str]=""):   #this is method by orm , setting query parameter limit to 10 by default

    print(limit)
    # posts = db.query(models.Post).filter(models.Post.owner_id==current_user.id).all() for getting posts of logged in user only
    
    # posts = db.query(models.Post).filter(models.Post.title.contains(search) ).limit(limit).offset(skip).all() 
    #    
    # cursor.execute(""" SELECT * FROM posts""")  this is traditional way of querying in sql
    # posts = cursor.fetchall()

    results = db.query(models.Post , func.count(models.Vote.post_id).label("votes")).join(models.Vote,models.Vote.post_id == models.Post.id, isouter = True).group_by(models.Post.id).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    # return posts
    return results 


@router.post("/",status_code=status.HTTP_201_CREATED, response_model=schemas.PostResponse)
def create_posts(post :schemas.PostCreate,db:Session = Depends(get_db),
                 current_user: int = Depends(oauth2.get_current_user)):
    # cursor.execute("""INSERT INTO posts (title , content , published) VALUES (%s,%s,%s) RETURNING * """,(post.title,post.content,post.published))
    # new_post=cursor.fetchone()
    # conn.commit()

    # new_post = models.Post(title=post.title, content=post.content, published=post.published)
    print("User ID:", current_user.id)
    # Print the user ID to verify it's being passed correctly
    
    new_post = models.Post(owner_id=current_user.id,**post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

    # post_dict=new_post.dict()
    # post_dict['id']= randrange(0,1000000)
    # my_posts.append(post_dict)
    # return {"Data": my_posts}


# def create_posts(payload:dict = Body(...)):
#     print(payload)
#     return{"new post": f"title: {payload['title']} content: {payload['content']}"}


@router.get("/{id}",response_model=schemas.PostOut)
def get_post(id : int , db:Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    # cursor.execute("""SELECT * FROM posts WHERE id =%s""",(str(id),))
    # post=cursor.fetchone()

    post=db.query(models.Post).filter(models.Post.id == id).first()

    post =db.query(models.Post , func.count(models.Vote.post_id).label("votes")).join(models.Vote,models.Vote.post_id == models.Post.id, isouter = True).group_by(models.Post.id).filter(models.Post.id == id).first()

    if not post:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} was not found")
    # if post.owner_id != current_user.id: #post is a query object so we need to use post.first().owner_id
    #     raise HTTPException(status.HTTP_403_FORBIDDEN, detail="Not authorized to perform requested action")

    return post

        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {"message": f"post with id: {id} was not found"} 
    
@router.delete("/{id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_posts(id :int, db:Session = Depends(get_db) , current_user: int = Depends(oauth2.get_current_user)):
    # cursor.execute("""DELETE FROM posts WHERE id =%s RETURNING *  """,(str(id),))
    # deleted_post=cursor.fetchone()
    # conn.commit()

    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()

    if post_query.first() == None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} does not exist")
    
    if post.owner_id != current_user.id: #post is a query object so we need to use post.first().owner_id
        raise HTTPException(status.HTTP_403_FORBIDDEN, detail="Not authorized to perform requested action")


    post_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.put("/{id}",response_model=schemas.PostResponse)
def update_post(id : int, updated_post:schemas.PostCreate, db:Session = Depends(get_db)
                ,  current_user: int = Depends(oauth2.get_current_user)):
    # cursor.execute("""UPDATE posts SET title = %s , content = %s where id = %s RETURNING *""",(post.title , post.content,str(id),))
    # updated_post=cursor.fetchone()
    # conn.commit()
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()

    if post == None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} was not found") 
    
    if post.owner_id != current_user.id: #post is a query object so we need to use post.first().owner_id
        raise HTTPException(status.HTTP_403_FORBIDDEN, detail="Not authorized to perform requested action")
    
    post_query.update(updated_post.dict(), synchronize_session=False)
    db.commit()

    return post_query.first()
