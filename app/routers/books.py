# app/routers/books.py
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from typing import List, Optional
from .. import crud, schemas
from ..database import get_db
from ..security import get_api_key

router = APIRouter(
    prefix="/items",
    tags=["items"],
)

@router.post("/", response_model=schemas.Book, status_code=status.HTTP_201_CREATED, dependencies=[Depends(get_api_key)])
def create_item(book: schemas.BookCreate, db: Session = Depends(get_db)):
    try:
        return crud.create_book(db=db, book=book)
    except IntegrityError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="A book with this title already exists.")

@router.put("/{item_id}", response_model=schemas.Book, dependencies=[Depends(get_api_key)])
def update_item(item_id: int, book: schemas.BookUpdate, db: Session = Depends(get_db)):
    updated_book = crud.update_book(db, book_id=item_id, book_update=book)
    if updated_book is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")
    return updated_book

@router.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT, dependencies=[Depends(get_api_key)])
def delete_item(item_id: int, db: Session = Depends(get_db)):
    deleted_book = crud.delete_book(db, book_id=item_id)
    if deleted_book is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")

@router.get("/", response_model=List[schemas.Book])
def read_items(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    author: Optional[str] = Query(None),
    sort_by: Optional[str] = Query(None, enum=["title", "author", "publication_date"]),
    sort_order: schemas.SortOrder = Query(schemas.SortOrder.ASC),
    db: Session = Depends(get_db)
):
    return crud.get_books(db, skip=skip, limit=limit, author=author, sort_by=sort_by, sort_order=sort_order)

@router.get("/{item_id}", response_model=schemas.Book)
def read_item(item_id: int, db: Session = Depends(get_db)):
    db_book = crud.get_book(db, book_id=item_id)
    if db_book is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")
    return db_book

@router.post("/transaction-demo/", response_model=List[schemas.Book], status_code=status.HTTP_201_CREATED, dependencies=[Depends(get_api_key)])
def create_multiple_items(books: List[schemas.BookCreate], db: Session = Depends(get_db)):
    if len(books) < 2:
        raise HTTPException(status_code=400, detail="This endpoint requires at least two books to demonstrate a transaction.")
    try:
        return crud.create_books_in_transaction(db=db, books=books)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
