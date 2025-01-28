import json
import uuid

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import Annotated, List, Dict
from sqlalchemy import or_, text
from .authen import get_current_user

from routers import get_db
from db.models import Book, User
from db.schemas import BookSchema, BookCreate

router = APIRouter(
    prefix="/book",
    tags=["book"],
    responses={404: {"description": "Not found"}},
)

@router.post("/", response_model=BookCreate)
async def create_book(
    book: BookCreate, db: Session = Depends(get_db)
):
    # Create a new Book instance and add it to the database
    new_book = Book(
        title=book.title,
        desc=book.desc,
        author=book.author,
        genre=book.genre,
        isbn=book.isbn,
        book_format=book.book_format,
        cover_img_url=book.cover_img_url,
        num_page=book.num_page,
        num_rate=book.num_rate,
        num_review=book.num_review,
        avg_rate=book.avg_rate,
    )
    
    # Add the new book to the session and commit
    db.add(new_book)
    db.commit()
    db.refresh(new_book)  # Refresh to get the new ID and other values
    
    return new_book

@router.get("/", response_model=list[BookSchema])
async def get_book(
    db: Session = Depends(get_db),
    title: Annotated[str | None, Query(title='Book title to search for')] = None,
    author: Annotated[List[str] | None, Query(title='Author name to search for')] = None,
    genre: Annotated[List[str] | None, Query(title='Genre to filter by')] = None,
    book_format: Annotated[str | None, Query(title='Book format to filter by')] = None,
    isbn: Annotated[str | None, Query(title='ISBN to filter by')] = None,
    current_user: User = Depends(get_current_user)
) -> list[BookSchema]:
    """
    Query Book.

    Parameters:
    - title: Filter by book title.
    - author: Filter by author.
    - genre: Filter by genre.
    - book_format: Filter by book format.
    - isbn: Filter by ISBN.

    Returns:
    List of Book.
    """
    query = db.query(Book)

    if title:
        query = query.filter(Book.title.ilike(f"%{title}%"))
    if author:
        query = query.filter(or_(*[Book.author.ilike(f"%{a}%") for a in author]))
    if genre:
        query = query.filter(or_(*[Book.genre.ilike(f"%{g}%") for g in genre]))
    if book_format:
        query = query.filter(Book.book_format.ilike(f"%{book_format}%"))
    if isbn:
        query = query.filter(Book.isbn.ilike(f"%{isbn}%"))

    query = query.limit(100)

    return query.all()


from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import Annotated, List
from sqlalchemy import or_
from .authen import get_current_user

from routers import get_db
from db.models import Book, User
from db.schemas import BookSchema, BookCreate

router = APIRouter(
    prefix="/book",
    tags=["book"],
    responses={404: {"description": "Not found"}},
)


@router.post("/", response_model=BookCreate)
async def create_book(
        book: BookCreate, db: Session = Depends(get_db)
):
    # Create a new Book instance and add it to the database
    new_book = Book(
        title=book.title,
        desc=book.desc,
        author=book.author,
        genre=book.genre,
        isbn=book.isbn,
        book_format=book.book_format,
        cover_img_url=book.cover_img_url,
        num_page=book.num_page,
        num_rate=book.num_rate,
        num_review=book.num_review,
        avg_rate=book.avg_rate,
    )

    # Add the new book to the session and commit
    db.add(new_book)
    db.commit()
    db.refresh(new_book)  # Refresh to get the new ID and other values

    return new_book


@router.get("/popular", response_model=list[BookSchema])
async def get_book_popular(
        db: Session = Depends(get_db),
) -> list[BookSchema]:
    datas=db.query(Book).order_by(Book.num_review, text("DESC")).limit(10).all()
    return datas


@router.get("/recommend", response_model=list[BookSchema])
async def get_book_recommend(
        db: Session = Depends(get_db),
)-> list[BookSchema]:
    datas=db.query(Book).order_by(Book.avg_rate, text("DESC")).limit(10).all()
    return datas
@router.get("/categories")
async def get_categories(db: Session = Depends(get_db)):
    datas=db.query(Book.genre).all()
    results = set()
    for data in datas:
        for i in data:
            results = results.union(set(list(i)))
    response = []
    for category in list(results):
        response.append({
            "name": category
        })
    return response
@router.get("/detail", response_model=BookSchema)
async def get_book_detail(
        db: Session = Depends(get_db),
        book_id: Annotated[str | None, Query(title='Book title to search for')] = None,
    ):
    datas = db.query(Book).filter(Book.book_id==book_id).one()
    return datas


@router.get("/text")
async def get_book_text(
    db: Session = Depends(get_db),
    book_id: Annotated[str | None, Query(title='Book title to search for')] = None,
):
    data = db.query(Book).filter(Book.book_id == book_id).one()
    if data:
        return {
            "title": data.title,
            "text": data.desc * 3
        }
    return {
        "title": "Error",
        "text": "Error get content book"
    }


@router.get("/search")
async def search_book(
        db: Session = Depends(get_db),
        title: Annotated[str | None, Query(title='Book title to search for')] = None,
)-> list[BookSchema]:
    query = db.query(Book)
    if title:
        query = query.filter(Book.title.ilike(f"%{title}%"))
    datas = query.limit(100).all()
    return datas

@router.get("/category")
async def search_book_by_category(
        db: Session = Depends(get_db),
        name: Annotated[str | None, Query(title='Book title to search for')] = None,
):
    query = db.query(Book)
    if name:
        query = query.filter(or_(*[Book.genre.ilike(f"%{name}%")]))
    datas = query.limit(100).all()
    return datas