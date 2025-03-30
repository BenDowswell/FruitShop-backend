### backend/app/routes/users.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import schemas, crud
from ..database import get_db

router = APIRouter(prefix="/users", tags=["Users"])


@router.post("/", response_model=schemas.UserOut)
def register_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    existing = crud.get_user_by_username(db, user.username)
    if existing:
        raise HTTPException(status_code=400, detail="Username already exists")
    return crud.create_user(db, user)


@router.get("/", response_model=list[schemas.User])
def list_users(db: Session = Depends(get_db)):
    """
    API endpoint to list all users.
    """
    return crud.list_all_users(db)
