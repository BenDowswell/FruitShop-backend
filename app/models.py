### backend/app/models.py

from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime, func
from sqlalchemy.orm import relationship
from .database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    password_hash = Column(String, nullable=False)
    role = Column(String, nullable=False)  # 'admin' or 'customer'

    carts = relationship("Cart", back_populates="user")


class Fruit(Base):
    __tablename__ = "fruits"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    prefix = Column(String(1), unique=True, nullable=False)
    price = Column(Float, nullable=False)
    quantity = Column(Integer, nullable=False)

    cart_items = relationship("CartItem", back_populates="fruit")


class Cart(Base):
    __tablename__ = "carts"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    user = relationship("User", back_populates="carts")
    items = relationship("CartItem", back_populates="cart")


class CartItem(Base):
    __tablename__ = "cart_items"

    id = Column(Integer, primary_key=True, index=True)
    cart_id = Column(Integer, ForeignKey("carts.id"))
    fruit_id = Column(Integer, ForeignKey("fruits.id"))
    quantity = Column(Integer, nullable=False)

    cart = relationship("Cart", back_populates="items")
    fruit = relationship("Fruit", back_populates="cart_items")
