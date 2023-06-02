import datetime
from enum import Enum
from typing import Optional
from uuid import UUID, uuid4
from pydantic import BaseModel, EmailStr

class Role(str, Enum):
    admin = 'admin'
    user = 'user'
    
class UserBase(BaseModel):
    email: str
    name: str
    email: EmailStr
    role: Role

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: Optional[UUID] = uuid4()


class PostBase(BaseModel):
    title: str
    content: str
    published: bool
    created_at: datetime.datetime
    updated_at: Optional[datetime.datetime]

class PostCreate(PostBase):
    pass

class Post(PostBase):
    id: Optional[int] = int()


class CommentBase(BaseModel):
    title: str
    content: str
    published: bool
    created_at: datetime.datetime
    updated_at: Optional[datetime.datetime]

class PostCreate(PostBase):
    pass

class Post(PostBase):
    id: Optional[int] = int()