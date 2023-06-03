import datetime
from enum import Enum
from typing import Optional
from uuid import UUID, uuid4
from pydantic import BaseModel, EmailStr, Field

class Role(str, Enum):
    admin = 'admin'
    user = 'user'
    
class CommentBase(BaseModel):
    content: str
    created_at: Optional[datetime.datetime]

class CommentCreate(CommentBase):
    created_at: Optional[datetime.datetime] = Field(default_factory=datetime.datetime.now)

class Comment(CommentBase):
    id: UUID
    post_id: UUID
    owner_id: UUID

    class Config:
        orm_mode = True

class PostBase(BaseModel):
    title: str
    content: str
    published: bool
    created_at: Optional[datetime.datetime] 

class PostCreate(PostBase):
    created_at: Optional[datetime.datetime] = Field(default_factory=datetime.datetime.now)

class Post(PostBase):
    id: UUID
    owner_id: UUID
    comments: list[Comment] = []

    class Config:
        orm_mode = True    


class UserBase(BaseModel):
    name: str
    email: EmailStr
    role: Role

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: UUID
    posts: list[Post] = []
    comments: list[Comment] = []

    class Config:
        orm_mode = True




