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
  - Install: `pip install fastapi`

- **Uvicorn (v0.20.0)**
  - ASGI server implementation for running FastAPI applications
  - Includes uvloop, httptools, and watchfiles for enhanced performance
  - Install: `pip install uvicorn[standard]`

#### Database Related
- **SQLAlchemy (v2.0.7)**
  - SQL toolkit and Object-Relational Mapping (ORM)
  - Install: `pip install sqlalchemy`

- **psycopg2-binary (v2.9.6)**
  - PostgreSQL adapter for Python
  - Install: `pip install psycopg2-binary`

- **PyMySQL (v1.0.3)**
  - MySQL client library
  - Install: `pip install PyMySQL`

#### Security & Authentication
- **python-jose (v3.3.0)**
  - Provides JWT token functionality
  - Includes rsa (v4.9) and ecdsa (v0.18.0) for cryptographic operations
  - Install: `pip install python-jose[cryptography]`

- **passlib (v1.7.4)**
  - Password hashing library
  - Works with bcrypt (v4.0.1)
  - Install: `pip install passlib[bcrypt]`

- **cryptography (v39.0.2)**
  - Cryptographic recipes and primitives
  - Install: `pip install cryptography`

- **python-multipart (v0.0.6)**
  - Handles form data parsing
  - Install: `pip install python-multipart`

#### Environment & Configuration
- **python-dotenv (v1.0.0)**
  - Loads environment variables from .env files
  - Install: `pip install python-dotenv`

- **PyYAML (v6.0)**
  - YAML parser and emitter
  - Install: `pip install PyYAML`

#### ASGI Server Components
- **uvloop (v0.17.0)**
  - Ultra-fast implementation of asyncio event loop
  - Install: `pip install uvloop`

- **httptools (v0.5.0)**
  - Fast HTTP parsing
  - Install: `pip install httptools`

- **watchfiles (v0.18.1)**
  - File system monitoring
  - Install: `pip install watchfiles`

- **websockets (v10.4)**
  - WebSocket client and server library
  - Install: `pip install websockets`

#### Additional Dependencies
- **pydantic (v1.10.5)**
  - Data validation using Python type annotations
  - Install: `pip install pydantic`

- **starlette (v0.26.1)**
  - Lightweight ASGI framework
  - Install: `pip install starlette`

- **typing_extensions (v4.5.0)**
  - Backported typing hints
  - Install: `pip install typing_extensions`

- **anyio (v3.6.2)**
  - Asynchronous networking and concurrency
  - Install: `pip install anyio`

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
git clone https://github.com/yourusername/fastapi_Learning.git
cd fastapi_Learning
pip install -r requirements.txt
```

### Running the Application

```bash
uvicorn main:app --reload
```

Visit [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs) for the interactive API documentation.

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