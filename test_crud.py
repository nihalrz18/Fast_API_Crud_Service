# tests/test_crud.py
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app import crud, models, schemas

# Setup an in-memory SQLite database for testing
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Fixture to create a new database for each test function
@pytest.fixture()
def db_session():
    models.Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    yield db
    db.close()
    models.Base.metadata.drop_all(bind=engine)

def test_create_and_get_book(db_session):
    """
    Unit test for creating and retrieving a book.
    """
    book_data = schemas.BookCreate(title="Test Book", author="Test Author")
    created_book = crud.create_book(db=db_session, book=book_data)
    
    assert created_book.title == "Test Book"
    assert created_book.author == "Test Author"
    assert created_book.id is not None
    
    retrieved_book = crud.get_book(db=db_session, book_id=created_book.id)
    assert retrieved_book.title == created_book.title
