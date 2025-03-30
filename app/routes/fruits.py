### backend/app/routes/fruits.py

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from .. import schemas, crud, auth
from ..database import get_db

router = APIRouter(prefix="/fruits", tags=["Fruits"])


@router.get("/", response_model=list[schemas.FruitOut])
def list_fruits(
    db: Session = Depends(get_db),
    current_user: schemas.UserOut = Depends(auth.get_current_user),
):
    return crud.get_all_fruits(db)


@router.post("/", response_model=schemas.FruitOut)
def add_fruit(
    fruit: schemas.FruitCreate,
    db: Session = Depends(get_db),
    current_user: schemas.UserOut = Depends(auth.get_current_user),
):
    return crud.create_fruit(db, fruit)
