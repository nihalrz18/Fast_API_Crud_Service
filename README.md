# FastAPI CRUD Service for Books

This project is a simple yet robust RESTful API built with FastAPI for managing a collection of books. It demonstrates best practices in API design, database interaction with SQLAlchemy, testing, and containerization with Docker.

## Features

- **Full CRUD Operations:** Create, Read, Update, and Delete books.
- **Data Validation:** Pydantic schemas for strict request/response validation.
- **Database Migrations:** Alembic for managing database schema changes.
- **Authentication:** Simple API key authentication for write operations.
- **Advanced Querying:** Pagination, filtering by author, and sorting.
- **Transaction Handling:** An endpoint to demonstrate atomic creation of multiple items.
- **Testing:** Comprehensive unit and integration tests with Pytest.
- **Containerization:** Fully containerized with Docker for easy deployment.

## Project Structure

. ├── alembic/ ├── app/ │ ├── routers/ │ │ └── books.py │ ├── crud.py │ ├── database.py │ ├── main.py │ ├── models.py │ ├── schemas.py │ └── security.py ├── tests/ ├── .dockerignore ├── alembic.ini ├── Dockerfile ├── README.md └── requirements.txt


## Setup and Installation

### 1. Prerequisites
- Python 3.9+
- Docker (for containerized deployment)

### 2. Local Setup
1.  **Clone the repository:**
    ```bash
    git clone <your-repo-url>
    cd fastapi_crud_service
    ```
2.  **Create and activate a virtual environment:**
    ```bash
    # Windows
    python -m venv venv
    .\venv\Scripts\activate

    # macOS/Linux
    python3 -m venv venv
    source venv/bin/activate
    ```
3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

### 3. Database Migration
Run the Alembic migrations to create the database tables:
```bash
alembic upgrade head
