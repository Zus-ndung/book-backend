import uuid
from sqlalchemy import Column, ForeignKey, Integer, String, Float, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID  # Use for PostgreSQL
from .database import Base


class User(Base):
    __tablename__ = "user"

    user_id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    username = Column(String, nullable=False)
    hash_password = Column(String, nullable=False)
    display_name = Column(String, nullable=False)
    type_authen = Column(String, nullable=False)


class Book(Base):
    __tablename__ = "book"

    book_id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    title = Column(String, nullable=False)
    desc = Column(String)
    author = Column(JSON, nullable=False)
    genre = Column(JSON)
    isbn = Column(String, unique=True)
    book_format = Column(String)
    cover_img_url = Column(String)
    num_page = Column(Integer, default=0)
    num_rate = Column(Integer, default=0)
    num_review = Column(Integer, default=0)
    avg_rate = Column(Float, default=0.0)


class Review(Base):
    __tablename__ = "review"

    review_id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String, ForeignKey("user.user_id"), nullable=False)
    book_id = Column(String, ForeignKey("book.book_id"), nullable=False)
    rating = Column(Integer, nullable=False)
    comment = Column(String)


class History(Base):
    __tablename__ = "history"

    history_id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String, ForeignKey("user.user_id"), nullable=False)
    type_event = Column(String, nullable=False)
    datetime = Column(String, nullable=False)