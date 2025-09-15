# app/main.py
from fastapi import FastAPI
from .routers import books
# We don't need these here anymore since Alembic handles DB creation
# from . import models
# from .database import engine

# This line is no longer needed; Alembic will manage the database schema.
# models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Book CRUD Service",
    description="A simple API to manage a collection of books.",
    version="1.0.0",
)

# Include the router for book-related endpoints
app.include_router(books.router)

@app.get("/", tags=["Root"])
def read_root():
    return {"message": "Welcome to the Book CRUD Service API!"}
