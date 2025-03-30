### backend/app/schemas.py

from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime


class UserBase(BaseModel):
    username: str


class UserCreate(UserBase):
    password: str
    role: str


class UserOut(UserBase):
    id: int
    role: str

    model_config = {"from_attributes": True}


class FruitBase(BaseModel):
    name: str
    prefix: str
    price: float
    quantity: int


class FruitCreate(FruitBase):
    pass


class FruitOut(FruitBase):
    id: int

    model_config = {"from_attributes": True}


class FruitUpdate(BaseModel):
    name: Optional[str]
    prefix: Optional[str]
    price: Optional[float]
    quantity: Optional[int]


class CartItemBase(BaseModel):
    fruit_id: int
    quantity: int


class CartItemCreate(CartItemBase):
    pass


class CartItemOut(CartItemBase):
    id: int
    fruit: FruitOut

    model_config = {"from_attributes": True}


class CartOut(BaseModel):
    id: int
    user_id: int
    created_at: datetime
    items: List[CartItemOut]

    model_config = {"from_attributes": True}


class Token(BaseModel):
    access_token: str
    token_type: str
