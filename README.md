# 🍊 Fruit Shop Backend (FastAPI + PostgreSQL)

This is the backend for the Fruit Shop web application. It provides a RESTful API using FastAPI and connects to a PostgreSQL database for managing users, fruits, and customer carts.

---

## 🚀 Features

- User registration (admin or customer)
- Fruit inventory management
- Cart creation and fruit purchases
- Fully tested with `pytest`
- PostgreSQL database integration
- Passwords hashed with `bcrypt`

---

## 🛠 Tech Stack

- **FastAPI** – web framework
- **SQLAlchemy** – ORM for PostgreSQL
- **Pydantic v2** – schema validation
- **pytest** – testing
- **Docker (optional)** – for local PostgreSQL setup

---

## 📦 Setup Instructions
### prereq db script:
    https://github.com/BenDowswell/Database/tree/main/frtuitshop
### 1. Clone the repo
```bash
git clone https://github.com/BenDowswell/fruit-shop-backend.git
cd fruit-shop-backend/backend
```
### 2. Create and activate a virtual environment
```bash
python3 -m venv venv
source venv/bin/activate  # Windows: venv\\Scripts\\activate
```
### 3.  Install dependencies
```bash
pip install -r requirements.txt
```
### 4. Set up environment variables
### Create a .env file based on this template:
```bash
DB_USER=postgres
DB_PASSWORD=postgres
DB_HOST=localhost
DB_PORT=5432
DB_NAME=fruitshop
Make sure your PostgreSQL database is running and matches these credentials.
```

### 5. Running Tests

PYTHONPATH=./ pytest -v

### 6. Run the API
uvicorn app.main:app --reload
Visit the docs at:
📘 http://localhost:8000/docs
