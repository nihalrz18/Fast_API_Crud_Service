# app/crud.py
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from typing import List
from . import models, schemas

# (This is the corrected and clean version from our previous discussion)
def get_book(db: Session, book_id: int):
    return db.query(models.Book).filter(models.Book.id == book_id).first()

def get_books(
    db: Session,
    skip: int = 0,
    limit: int = 100,
    author: str = None,
    sort_by: str = None,
    sort_order: schemas.SortOrder = schemas.SortOrder.ASC
):
    query = db.query(models.Book)
    if author:
        query = query.filter(models.Book.author.ilike(f"%{author}%"))
    if sort_by:
        sort_column = getattr(models.Book, sort_by, None)
        if sort_column:
            if sort_order == schemas.SortOrder.DESC:
                query = query.order_by(sort_column.desc())
            else:
                query = query.order_by(sort_column.asc())
    return query.offset(skip).limit(limit).all()

def create_book(db: Session, book: schemas.BookCreate):
    db_book = models.Book(**book.model_dump())
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book

def update_book(db: Session, book_id: int, book_update: schemas.BookUpdate):
    db_book = get_book(db, book_id)
    if not db_book:
        return None
    update_data = book_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_book, key, value)
    db.commit()
    db.refresh(db_book)
    return db_book

def delete_book(db: Session, book_id: int):
    db_book = get_book(db, book_id)
    if not db_book:
        return None
    db.delete(db_book)
    db.commit()
    return db_book

def create_books_in_transaction(db: Session, books: List[schemas.BookCreate]):
    created_books = []
    try:
        for book_data in books:
            db_book = models.Book(**book_data.model_dump())
            db.add(db_book)
        db.commit()
        for instance in db.query(models.Book).filter(models.Book.id.in_([b.id for b in db.new])).all():
            created_books.append(instance)
    except IntegrityError as e:
        db.rollback()
        raise ValueError(f"Transaction failed: {e.orig}")
    return created_books
