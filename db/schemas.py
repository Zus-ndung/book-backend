from pydantic import BaseModel, Field
from typing import Optional, List
import uuid

class UserSchema(BaseModel):
    user_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    username: str
    hash_password: str
    display_name: str
    type_authen: str

    class Config:
        orm_mode = True

class UserCreate(BaseModel):
    username: str
    password: str
    display_name: str
    type_authen: str

    class Config:
        orm_mode = True

class Token(BaseModel):
    access_token: str
    token_type: str


class BookSchema(BaseModel):
    book_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    title: str
    desc: Optional[str] = None
    author: List[str]  # List of authors
    genre: Optional[List[str]] = None  # List of genres
    isbn: Optional[str] = None
    book_format: Optional[str] = None
    cover_img_url: Optional[str] = None
    num_page: Optional[int] = 0
    num_rate: Optional[int] = 0
    num_review: Optional[int] = 0
    avg_rate: Optional[float] = 0.0

    class Config:
        orm_mode = True


class BookCreate(BaseModel):
    title: str
    desc: Optional[str] = None
    author: List[str]  # List of authors
    genre: Optional[List[str]] = None  # List of genres
    isbn: Optional[str] = None
    book_format: Optional[str] = None
    cover_img_url: Optional[str] = None
    num_page: Optional[int] = None
    num_rate: Optional[int] = None
    num_review: Optional[int] = None
    avg_rate: Optional[float] = None

    class Config:
        orm_mode = True


class ReviewSchema(BaseModel):
    review_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    user_id: str
    book_id: str
    rating: int
    comment: Optional[str]

    class Config:
        orm_mode = True

class ReviewCreate(BaseModel):
    user_id: str
    book_id: str
    rating: int
    comment: str | None = None  # Optional comment

    class Config:
        orm_mode = True


class HistorySchema(BaseModel):
    history_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    user_id: str
    type_event: str
    datetime: str

    class Config:
        orm_mode = True

class HistoryCreate(BaseModel):
    user_id: str
    type_event: str
    datetime: str

    class Config:
        orm_mode = True

class UserMeSchema(BaseModel):
    user_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    username: str
    display_name: str

    class Config:
        orm_mode = True