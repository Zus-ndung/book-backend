from fastapi import APIRouter, Depends, Query, HTTPException, status
from sqlalchemy.orm import Session
from typing import Annotated

from routers import get_db
from .authen import get_current_user
from db.models import Review, User, Book
from db.schemas import ReviewSchema, ReviewCreate

router = APIRouter(
    prefix="/review",
    tags=["review"],
    responses={404: {"description": "Not found"}},
)

@router.get("/", response_model=list[ReviewSchema])
async def get_review(
    db: Session = Depends(get_db),
    user_id: Annotated[str | None, Query(title='Filter by user ID')] = None,
    book_id: Annotated[str | None, Query(title='Filter by book ID')] = None,
    rating_min: Annotated[int | None, Query(title='Minimum rating')] = None,
    rating_max: Annotated[int | None, Query(title='Maximum rating')] = None,
    current_user: User = Depends(get_current_user)
) -> list[ReviewSchema]:
    """
    Query Review.

    Parameters:
    - user_id: Filter by user ID.
    - book_id: Filter by book ID.
    - rating_min: Minimum rating value.
    - rating_max: Maximum rating value.

    Returns:
    List of Review.
    """
    query = db.query(Review)

    if user_id:
        query = query.filter(Review.user_id == user_id)
    if book_id:
        query = query.filter(Review.book_id == book_id)
    if rating_min is not None:
        query = query.filter(Review.rating >= rating_min)
    if rating_max is not None:
        query = query.filter(Review.rating <= rating_max)

    return query.all()

@router.post("/", response_model=ReviewSchema)
async def create_review(
    review: ReviewCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)
):
    """
    Create a new review.
    """
    # Ensure the user exists (or other validation logic, like book existence)
    if db.query(User).filter(User.user_id == review.user_id).first() is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User does not exist"
        )

    if db.query(Book).filter(Book.book_id == review.book_id).first() is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Book does not exist"
        )

    # Create a new Review instance
    new_review = Review(
        user_id=review.user_id,
        book_id=review.book_id,
        rating=review.rating,
        comment=review.comment
    )

    # Add the review to the session and commit it to the database
    db.add(new_review)
    db.commit()
    db.refresh(new_review)

    return new_review