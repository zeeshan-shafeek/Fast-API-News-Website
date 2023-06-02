from sqlalchemy import UUID, Column, ForeignKey, String, Boolean, DateTime
from sqlalchemy.orm import relationship
from .database import Base
import uuid


class User(Base):
    __tablename__ = 'users'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String)
    email = Column(String)
    hashed_password = Column(String)
    role = Column(String)

    posts = relationship('Post', back_populates= 'owner')
    comments = relationship('Comment', back_populates= 'owner')

class Post(Base):
    __tablename__ = 'posts'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = Column(String)
    content = Column(String)
    published = Column(Boolean)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)
    owner_id = Column(UUID, ForeignKey("users.id"))

    owner = relationship("User", back_populates="posts")
    comments = relationship('Comment', back_populates= 'post')

class Comment(Base):
    __tablename__ = 'comments'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    content = Column(String)
    created_at = Column(DateTime)
    owner_id = Column(UUID, ForeignKey("users.id"))
    post_id = Column(UUID, ForeignKey("posts.id"))
    
    owner = relationship("User", back_populates= "comments")
    post = relationship("Post", back_populates= "comments")