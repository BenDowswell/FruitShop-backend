### backend/app/routes/fruits.py

from fastapi import APIRouter, Depends, HTTPException
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
    # Restrict this route to admins only
    auth.require_role(current_user, "admin")
    return crud.create_fruit(db, fruit)


@router.put("/{fruit_id}", response_model=schemas.FruitOut)
def update_fruit(
    fruit_id: int,
    fruit_data: schemas.FruitUpdate,
    db: Session = Depends(get_db),
    current_user: schemas.UserOut = Depends(auth.get_current_user),
):
    # Restrict this route to admins only
    auth.require_role(current_user, "admin")

    updated_fruit = crud.update_fruit(db, fruit_id, fruit_data)
    if not updated_fruit:
        raise HTTPException(status_code=404, detail="Fruit not found")
    return updated_fruit


@router.delete("/{fruit_id}", status_code=204)
def delete_fruit(
    fruit_id: int,
    db: Session = Depends(get_db),
    current_user: schemas.UserOut = Depends(auth.get_current_user),
):
    # Restrict this route to admins only
    auth.require_role(current_user, "admin")

    db_fruit = db.query(models.Fruit).filter(models.Fruit.id == fruit_id).first()
    if not db_fruit:
        raise HTTPException(status_code=404, detail="Fruit not found")
    db.delete(db_fruit)
    db.commit()
    return
