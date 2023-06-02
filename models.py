from sqlalchemy import UUID, Column, ForeignKey, Integer, String, Boolean, DateTime
from sqlalchemy.orm import relationship
from config import Base


class User(Base):
    __tablename__ = 'users'

    id = Column(UUID, primary_key=True, index=True)
    name = Column(String)
    email = Column(String)
    hashed_password = Column(String)
    role: Column(String)

    posts = relationship('Post', back_populates= 'owner')

class Post(Base):
    __tablename__ = 'posts'

    id = Column(Integer, primary_key=True, index= True)
    title = Column(String)
    content = Column(String)
    published = Column(Boolean)
    created_at = Column(DateTime.datetime)
    updated_at = Column(DateTime.datetime)
    owner_id = Column(UUID, ForeignKey("users.id"))

    owner = relationship("User", back_populates="posts")

class Comment(Base):
    __tablename__ = 'comments'

    id = Column(Integer, primary_key=True, index= True)
    content = Column(String)
    created_at = Column(DateTime.datetime)
    owner_id = Column(UUID, ForeignKey("users.id"))
    
    owner = relationship("User", back_populates="comments")