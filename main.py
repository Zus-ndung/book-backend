from fastapi import FastAPI
from db import models
from db.database import engine
from routers import authen, book, review, history

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Include routers
app.include_router(authen.router)
app.include_router(book.router)
app.include_router(review.router)
app.include_router(history.router)