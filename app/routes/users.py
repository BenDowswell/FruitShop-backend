### backend/app/routes/users.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import schemas, crud, auth
from ..database import get_db

router = APIRouter(prefix="/users", tags=["Users"])


@router.post("/", response_model=schemas.UserOut)
def create_user(
    user: schemas.UserCreate,
    db: Session = Depends(get_db),
    current_user: schemas.UserOut = Depends(auth.get_current_user),
):
    # Restrict this route to admins only
    auth.require_role(current_user, "admin")
    return crud.create_user(db, user)


@router.get("/", response_model=list[schemas.UserOut])
def get_users(db: Session = Depends(get_db)):
    return crud.get_all_users(db)
