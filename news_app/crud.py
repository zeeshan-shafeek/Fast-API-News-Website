from uuid import UUID
from sqlalchemy.orm import Session
from . import models, schemas
from passlib.context import CryptContext

pwd_context = CryptContext(schemes= ["bcrypt"], deprecated= "auto")

def get_user(db: Session, user_id: UUID):
    return db.query(models.User).filter(models.User.id == user_id).first()

def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()

def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()

def create_user(db: Session, user: schemas.UserCreate):
    hashed_password = pwd_context.hash(user.password)
    db_user = models.User(name= user.name,
                          email= user.email,
                          role= user.role,
                          hashed_password= hashed_password
                          )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_posts(db: Session, skip: int = 0, limit: int =100):
    return db.query(models.Post).order_by(models.Post.created_at.desc()).offset(skip).limit(limit).all()

def create_user_post(db: Session, post: schemas.PostCreate, user_id: UUID):
    db_post = models.Post(**post.dict(), owner_id= user_id)
    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    return db_post

def get_post(db: Session, post_id: UUID):
    return db.query(models.Post).filter(models.Post.id == post_id).first()

def delete_post(db: Session, post_id: UUID):
    return db.query(models.Post).filter(models.Post.id == post_id).delete()


def create_user_comment(db: Session, comment: schemas.CommentCreate, user_id: UUID, post_id: UUID):
    db_comment = models.Comment(**comment.dict(), owner_id= user_id, post_id= post_id)
    db.add(db_comment)
    db.commit()
    db.refresh(db_comment)
    return db_comment

def get_post_comments(db: Session, post_id: UUID, skip: int = 0, limit: int =100):
    return db.query(models.Post).order_by(models.Comment.created_at.desc()).filter(post_id= post_id).offset(skip).limit(limit).all()

def delete_comment(db: Session, comment_id: UUID):
    return db.query(models.Comment).filter(models.Comment.id == comment_id).delete()