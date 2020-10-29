import datetime

from fastapi import Query
from pydantic import BaseModel
from typing import List, Optional

from const import OrderStatusValues


# User Schema

class UserBase(BaseModel):
    email: str = Query(None, min_length=3)


class UserCreate(UserBase):
    is_owner: bool
    password: str = Query(None, min_length=3)


class UserLogin(UserBase):
    password: str = Query(None, min_length=3)


class User(UserBase):
    id: int
    token: Optional[str] = None
    token_valid_until: Optional[datetime.datetime] = None
    is_owner: bool

    class Config:
        orm_mode = True


# Restaurant Schema
class RestaurantBase(BaseModel):
    name: str
    description: str


class RestaurantCreate(RestaurantBase):
    pass


class RestaurantUpdate(RestaurantBase):
    id: int


class Restaurant(RestaurantBase):
    id: int
    owner_id: int

    class Config:
        orm_mode = True


# Meal Schema
class MealBase(BaseModel):
    name: str
    description: str
    price: float


class MealCreate(MealBase):
    restaurant_id: int


class MealUpdate(MealCreate):
    id: int


class Meal(MealBase):
    id: int
    restaurant: Restaurant

    class Config:
        orm_mode = True


# Order Ban Schema
class OrderBan(BaseModel):
    user_id: int


# Order History Schema
class OrderHistoryBase(BaseModel):
    order_id: int
    status: OrderStatusValues


class OrderHistoryUpdate(OrderHistoryBase):
    pass


class OrderHistory(OrderHistoryBase):
    updated_on: datetime.datetime

    class Config:
        orm_mode = True


# Order Line Schema
class OrderLine(BaseModel):
    meal: Meal
    quantity: int

    class Config:
        orm_mode = True


# Order Schema
class OrderBase(BaseModel):
    pass


class OrderCreate(OrderBase):
    restaurant_id: int
    meal_ids: List[int]


class Order(OrderBase):
    id: int
    restaurant: Restaurant
    total: float
    lines: List[OrderLine]
    history: List[OrderHistory]
    user: User

    class Config:
        orm_mode = True
