# FastAPI Learning Project

This project is a learning exercise using [FastAPI](https://fastapi.tiangolo.com/), a modern, fast (high-performance) web framework for building APIs with Python 3.7+.

## Features

- RESTful API endpoints
- Asynchronous request handling
- Easy-to-read code structure
- Automatic interactive API docs (Swagger UI & ReDoc)

## Getting Started

### Prerequisites

- Python 3.7+
- [pip](https://pip.pypa.io/en/stable/)

### Dependencies

This project relies on the following Python packages. Here's a comprehensive breakdown:

#### Core Dependencies
- **FastAPI (v0.95.0)**
  - Modern web framework for building APIs
  - Provides high performance, automatic API documentation, and data validation

- **Uvicorn (v0.20.0)**
  - ASGI server implementation for running FastAPI applications
  - Includes uvloop, httptools, and watchfiles for enhanced performance

#### Database Related
- **SQLAlchemy (v2.0.7)**
  - SQL toolkit and Object-Relational Mapping (ORM)

- **psycopg2-binary (v2.9.6)**
  - PostgreSQL adapter for Python

- **PyMySQL (v1.0.3)**
  - MySQL client library

#### Security & Authentication
- **python-jose (v3.3.0)**
  - Provides JWT token functionality
  - Includes rsa (v4.9) and ecdsa (v0.18.0) for cryptographic operations

- **passlib (v1.7.4)**
  - Password hashing library
  - Works with bcrypt (v4.0.1)

- **cryptography (v39.0.2)**
  - Cryptographic recipes and primitives

- **python-multipart (v0.0.6)**
  - Handles form data parsing

#### Environment & Configuration
- **python-dotenv (v1.0.0)**
  - Loads environment variables from .env files

- **PyYAML (v6.0)**
  - YAML parser and emitter

#### ASGI Server Components
- **uvloop (v0.17.0)**
  - Ultra-fast implementation of asyncio event loop

- **httptools (v0.5.0)**
  - Fast HTTP parsing

- **watchfiles (v0.18.1)**
  - File system monitoring

- **websockets (v10.4)**
  - WebSocket client and server library

#### Additional Dependencies
- **pydantic (v1.10.5)**
  - Data validation using Python type annotations

- **starlette (v0.26.1)**
  - Lightweight ASGI framework

- **typing_extensions (v4.5.0)**
  - Backported typing hints

- **anyio (v3.6.2)**
  - Asynchronous networking and concurrency

- Other supporting packages:
  - click (v8.1.3)
  - idna (v3.4)
  - h11 (v0.14.0)
  - six (v1.16.0)
  - sniffio (v1.3.0)
  - cffi (v1.15.1)
  - pyasn1 (v0.4.8)
  - pycparser (v2.21)

#### Quick Installation
To install all dependencies at once, use:
```bash
pip install -r requirements.txt
```

#### Version Management
To ensure compatibility, this project uses specific versions of each package. If you need to update any dependency, please test thoroughly before deploying to production.

### Installation

```bash
git clone https://github.com/AlexDenkko/fastapi_Learning.git
cd fastapi_Learning
pip install -r requirements.txt
```

### Running the Application

```bash
uvicorn main:app --reload
```

Visit [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs) for the interactive API documentation.

### Testing with pytest

#### Test Dependencies
First, install the required testing packages:
```bash
pip install pytest pytest-asyncio httpx
```

#### Test Structure
The tests are located in the `test/` directory and follow this structure:
- `test_admin.py`: Admin functionality tests
- `test_auth.py`: Authentication tests
- `test_todos.py`: Todo operations tests
- `test_users.py`: User management tests
- `utils.py`: Testing utilities and fixtures

#### Running Tests
To run all tests:
```bash
pytest
```

To run specific test files:
```bash
pytest test/test_auth.py    # Run auth tests only
pytest test/test_todos.py   # Run todo tests only
```

To run tests with detailed output:
```bash
pytest -v
```

To see print statements during tests:
```bash
pytest -s
```

To run a specific test function:
```bash
pytest test/test_auth.py::test_function_name
```

#### Test Coverage
To check test coverage:
```bash
pip install pytest-cov
pytest --cov=app tests/
```

#### Writing Tests
Example of a test file structure:
```python
import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello World"}
```

## Project Structure

```
fastapi_Learning/
├── LICENSE
├── README.md
├── fastapi/
│   ├── test.db
│   └── TodoApp/
│       ├── database.py          # Database configuration and session management
│       ├── main.py             # FastAPI application entry point
│       ├── models.py           # SQLAlchemy database models
│       ├── todosapp.db         # SQLite database file
│       ├── routers/
│       │   ├── admin.py        # Admin panel routes
│       │   ├── auth.py         # Authentication routes
│       │   ├── todos.py        # Todo CRUD operations
│       │   └── users.py        # User management routes
│       ├── static/
│       │   ├── css/
│       │   │   ├── base.css
│       │   │   └── bootstrap.css
│       │   └── js/
│       │       ├── base.js
│       │       ├── bootstrap.js
│       │       ├── jquery-slim.js
│       │       └── popper.js
│       ├── templates/
│       │   ├── add-todo.html   # Todo creation form
│       │   ├── edit-todo.html  # Todo editing form
│       │   ├── home.html       # Dashboard page
│       │   ├── layout.html     # Base template
│       │   ├── login.html      # Authentication page
│       │   ├── navbar.html     # Navigation component
│       │   ├── register.html   # User registration
│       │   └── todo.html       # Todo detail view
│       └── test/
│           ├── __init__.py
│           ├── test_admin.py   # Admin functionality tests
│           ├── test_auth.py    # Authentication tests
│           ├── test_todos.py   # Todo operations tests
│           ├── test_users.py   # User management tests
│           └── utils.py        # Testing utilities
```

### Directory Structure Explanation

- `database.py`: Handles database connection and session management
- `main.py`: Application entry point and FastAPI configuration
- `models.py`: Database models using SQLAlchemy ORM
- `routers/`: Module containing route handlers
  - `admin.py`: Administrative endpoints
  - `auth.py`: Authentication and authorization
  - `todos.py`: Todo item management
  - `users.py`: User operations
- `static/`: Static assets (CSS, JavaScript)
- `templates/`: Jinja2 HTML templates
- `test/`: Unit and integration tests

## License

This project is licensed under the MIT License.

### MySQL Integration

#### Setting up MySQL
1. Install MySQL Server if not already installed:
   - Download MySQL installer from [official website](https://dev.mysql.com/downloads/installer/)
   - Run the installer and follow the setup wizard
   - Remember your root password

2. Create a new database and user:
```sql
CREATE DATABASE fastapi_db;
CREATE USER 'fastapi_user'@'localhost' IDENTIFIED BY 'your_password';
GRANT ALL PRIVILEGES ON fastapi_db.* TO 'fastapi_user'@'localhost';
FLUSH PRIVILEGES;
```

#### Database Configuration
1. Update your `.env` file with MySQL credentials:
```ini
DATABASE_URL=mysql+pymysql://fastapi_user:your_password@localhost:3306/fastapi_db
```

2. Modify `database.py` to use MySQL:
```python
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os

load_dotenv()

SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    # Remove 'connect_args' as it's only needed for SQLite
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
```

#### Required Dependencies
Ensure these packages are installed:
```bash
pip install pymysql cryptography
```

#### Database Migrations
1. Install Alembic for database migrations:
```bash
pip install alembic
```

2. Initialize Alembic:
```bash
alembic init alembic
```

3. Update `alembic.ini` with your database URL:
```ini
sqlalchemy.url = mysql+pymysql://fastapi_user:your_password@localhost:3306/fastapi_db
```

4. Create a migration:
```bash
alembic revision --autogenerate -m "Initial migration"
```

5. Apply migrations:
```bash
alembic upgrade head
```

#### Troubleshooting MySQL Connection
Common issues and solutions:

1. Connection refused:
   - Ensure MySQL service is running:
     ```bash
     # Windows
     net start mysql80
     
     # Check status
     net status mysql80
     ```

2. Authentication failed:
   - Verify credentials in `.env` file
   - Check user privileges:
     ```sql
     SHOW GRANTS FOR 'fastapi_user'@'localhost';
     ```

3. Database doesn't exist:
   ```sql
   CREATE DATABASE fastapi_db;
   ```

4. Reset user password if needed:
   ```sql
   ALTER USER 'fastapi_user'@'localhost' IDENTIFIED BY 'new_password';
   FLUSH PRIVILEGES;
   ```

#### Backup and Restore
Create database backup:
```bash
mysqldump -u fastapi_user -p fastapi_db > backup.sql
```

Restore database:
```bash
mysql -u fastapi_user -p fastapi_db < backup.sql
```