from uuid import UUID
from sqlalchemy.orm import Session

from fastapi import Depends, FastAPI, HTTPException
from . import models, crud, schemas
from .database import engine, SessionLocal
from pydantic import BaseModel

models.Base.metadata.create_all(bind= engine)

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get('/',)
def home(db: Session= Depends(get_db)):
    return {"status": "ok"}

@app.post("/users/", response_model= schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail='email already registered')
    return crud.create_user(db=db, user=user)

@app.get("/users/", response_model= list[schemas.User])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = crud.get_users(db, skip=skip, limit=limit)
    return users

@app.get("/users/{user_id}/", response_model= schemas.User)
def read_user(user_id: UUID, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, details= "User not found")
    return db_user

@app.post("/user/{user_id}/post/", response_model= schemas.Post)
def create_post_for_user(
    user_id: UUID,
    post: schemas.PostCreate,
    db: Session = Depends(get_db)
):
    return crud.create_user_post(db= db, post=post, user_id= user_id)

@app.post("/user/{user_id}/{post_id}/comment/", response_model= schemas.Post)
def create_comment_for_user(
    user_id: UUID,
    post_id: UUID,
    comment: schemas.CommentCreate,
    db: Session = Depends(get_db)
):
    return crud.create_user_comment(db= db, post_id=post_id, user_id= user_id, comment=comment)

@app.get("/posts/", response_model= list[schemas.Post])
def all_posts(skip: int = 0, limit: int =100, db: Session = Depends(get_db)):
    posts = crud.get_posts(db= db, skip=skip, limit=limit)
    return posts

@app.get("/post/{post_id}/", response_model= schemas.Post)
def read_post(post_id: UUID, db: Session = Depends(get_db)):
    post = crud.get_post(db= db, post_id= post_id)
    return post

@app.delete("/post/{post_id}/", response_class= schemas.Comment)
def delete_post(post_id: UUID, db: Session = Depends(get_db)):
    deleted_comment = crud.delete_post(db, post_id= post_id)
    return deleted_comment

@app.get("/post/{post_id}/comments/", response_class= list[schemas.Comment])
def read_post_comment(post_id: UUID, db: Session = Depends(get_db)):
    post_comments = crud.get_post_comments(db, post_id= post_id, skip= skip, limit= limit)
    return post_comments

@app.delete("/post/{post_id}/comment/{comment_id}/", response_class= schemas.Comment)
def delete_post_comment(comment_id: UUID, db: Session = Depends(get_db)):
    deleted_comment = crud.delete_comment(db, comment_id= comment_id)
    return deleted_comment