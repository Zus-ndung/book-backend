from fastapi import APIRouter, HTTPException, status, Depends, Query
from sqlalchemy.orm import Session
from typing import Annotated

from routers import get_db
from db.models import History, User
from db.schemas import HistorySchema, HistoryCreate
from .authen import get_current_user

router = APIRouter(
    prefix="/history",
    tags=["history"],
    responses={404: {"description": "Not found"}},
)

@router.get("/", response_model=list[HistorySchema])
async def get_history(
    db: Session = Depends(get_db),
    user_id: Annotated[str | None, Query(title='Filter by user ID')] = None,
    type_event: Annotated[str | None, Query(title='Filter by event type')] = None,
    datetime_min: Annotated[str | None, Query(title='Minimum datetime')] = None,
    datetime_max: Annotated[str | None, Query(title='Maximum datetime')] = None,
    current_user: User = Depends(get_current_user)
) -> list[HistorySchema]:
    """
    Query History.

    Parameters:
    - user_id: Filter by user ID.
    - type_event: Filter by event type.
    - datetime_min: Minimum datetime.
    - datetime_max: Maximum datetime.

    Returns:
    List of History entries.
    """
    query = db.query(History)

    if user_id:
        query = query.filter(History.user_id == user_id)
    if type_event:
        query = query.filter(History.type_event.ilike(f"%{type_event}%"))
    if datetime_min:
        query = query.filter(History.datetime >= datetime_min)
    if datetime_max:
        query = query.filter(History.datetime <= datetime_max)

    return query.all()


@router.post("/", response_model=HistoryCreate)
async def create_history(
    history: HistoryCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)
):
    """
    Create a new history entry.
    """
    # Ensure the user exists (or other validation logic)
    if db.query(User).filter(User.user_id == history.user_id).first() is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User does not exist"
        )
    
    # Create a new History instance
    new_history = History(
        user_id=history.user_id,
        type_event=history.type_event,
        datetime=history.datetime
    )

    db.add(new_history)
    db.commit()
    db.refresh(new_history)
    
    return new_history