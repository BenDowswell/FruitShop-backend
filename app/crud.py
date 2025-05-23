### backend/app/crud.py

from sqlalchemy.orm import Session
from . import models, schemas, auth
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# === User ===
def get_user_by_username(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()


def create_user(db: Session, user: schemas.UserCreate):
    hashed_password = auth.hash_password(user.password)
    db_user = models.User(
        username=user.username,
        password_hash=hashed_password,
        role=user.role or "customer",  # Default role is "customer"
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def list_all_users(db: Session):
    """
    Retrieve all users from the database.
    """
    return db.query(models.User).all()


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def authenticate_user(db: Session, username: str, password: str):
    user = get_user_by_username(db, username)
    if not user or not verify_password(password, user.password_hash):
        return None
    return user


# === Fruits ===
def get_all_fruits(db: Session):
    return db.query(models.Fruit).all()


def create_fruit(db: Session, fruit: schemas.FruitCreate):
    db_fruit = models.Fruit(**fruit.model_dump())
    db.add(db_fruit)
    db.commit()
    db.refresh(db_fruit)
    return db_fruit


def update_fruit(db: Session, fruit_id: int, fruit_data: schemas.FruitCreate):
    """
    Update the details of a fruit (e.g., price, quantity).
    """
    db_fruit = db.query(models.Fruit).filter(models.Fruit.id == fruit_id).first()
    if not db_fruit:
        return None
    for key, value in fruit_data.model_dump().items():
        setattr(db_fruit, key, value)
    db.commit()
    db.refresh(db_fruit)
    return db_fruit


# === Carts ===
def create_cart(db: Session, user_id: int):
    cart = models.Cart(user_id=user_id)
    db.add(cart)
    db.commit()
    db.refresh(cart)
    return cart


def add_fruit_to_cart(db: Session, cart_id: int, fruit_id: int, quantity: int):
    item = models.CartItem(cart_id=cart_id, fruit_id=fruit_id, quantity=quantity)
    db.add(item)
    db.commit()
    db.refresh(item)
    return item


def get_cart_with_items(db: Session, cart_id: int):
    return db.query(models.Cart).filter(models.Cart.id == cart_id).first()
