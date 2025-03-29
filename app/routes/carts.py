### backend/app/routes/carts.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import schemas, crud
from ..database import get_db

router = APIRouter(prefix="/carts", tags=["Carts"])

@router.post("/{user_id}", response_model=schemas.CartOut)
def create_new_cart(user_id: int, db: Session = Depends(get_db)):
    return crud.create_cart(db, user_id)

@router.post("/{cart_id}/items", response_model=schemas.CartItemOut)
def add_item_to_cart(cart_id: int, item: schemas.CartItemCreate, db: Session = Depends(get_db)):
    return crud.add_fruit_to_cart(db, cart_id, item.fruit_id, item.quantity)

@router.get("/{cart_id}", response_model=schemas.CartOut)
def get_cart(cart_id: int, db: Session = Depends(get_db)):
    cart = crud.get_cart_with_items(db, cart_id)
    if not cart:
        raise HTTPException(status_code=404, detail="Cart not found")
    return cart
