### backend/app/schemas.py

from pydantic import BaseModel, EmailStr
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


class User(BaseModel):
    username: str
    role: str

    class Config:
        orm_mode = True


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
<<<<<<< HEAD
=======


class TokenData(BaseModel):
    username: Optional[str] = None


class Login(BaseModel):
    username: str
    password: str
>>>>>>> refs/remotes/origin/master
