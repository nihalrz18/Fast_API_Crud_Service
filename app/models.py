# app/models.py
from sqlalchemy import Column, Integer, String, Date
from .database import Base

class Book(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, unique=True, nullable=False, index=True)
    author = Column(String, nullable=False)
    publication_date = Column(Date)
