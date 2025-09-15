# app/schemas.py
from pydantic import BaseModel
from datetime import date
from enum import Enum
from typing import Optional

class SortOrder(str, Enum):
    ASC = "asc"
    DESC = "desc"

class BookBase(BaseModel):
    title: str
    author: str
    publication_date: Optional[date] = None

class BookCreate(BookBase):
    pass

class BookUpdate(BaseModel):
    title: Optional[str] = None
    author: Optional[str] = None
    publication_date: Optional[date] = None

class Book(BookBase):
    id: int

    class Config:
        from_attributes = True
