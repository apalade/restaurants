import datetime

from sqlalchemy import Boolean, Column, ForeignKey, Integer,\
    String, Float, Enum, DateTime
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.hybrid import hybrid_property

from database import Base
from const import OrderStatusValues


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    password = Column(String)
    token = Column(String, default=None)
    token_valid_until = Column(DateTime, default=None)
    is_owner = Column(Boolean)
    is_ban = Column(Boolean, default=False)

    orders = relationship("Order")


class Restaurant(Base):
    __tablename__ = "restaurants"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(String, nullable=False)
    owner_id = Column(Integer, ForeignKey("users.id"))
    deleted = Column(Boolean, default=False)


class OrderHistory(Base):
    __tablename__ = "order_history"

    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("orders.id"))
    status = Column(Enum(OrderStatusValues))
    updated_on = Column(DateTime, default=datetime.datetime.utcnow)


class OrderLine(Base):
    __tablename__ = "order_lines"

    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("orders.id"), nullable=False)
    meal_id = Column(Integer, ForeignKey("meals.id"), nullable=False)
    quantity = Column(Integer, nullable=False)

    meal = relationship("Meal", cascade="all, delete")


class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    restaurant_id = Column(Integer, ForeignKey("restaurants.id"))
    user_id = Column(Integer, ForeignKey("users.id"))

    history = relationship(OrderHistory, cascade="all,delete")
    restaurant = relationship(Restaurant,
                              backref=backref('restaurant_orders',
                                              cascade="all,delete"))
    lines = relationship("OrderLine", cascade="all,delete")
    user = relationship("User")

    @hybrid_property
    def total(self):
        if self.lines:
            return sum([line.meal.price * line.quantity
                        for line in self.lines])
        return 0


class Meal(Base):
    __tablename__ = "meals"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    description = Column(String)
    price = Column(Float)
    restaurant_id = Column(Integer, ForeignKey("restaurants.id"),
                           nullable=False)
    restaurant = relationship(Restaurant, backref=backref(
        'restaurants', cascade=('all,delete')))

    lines = relationship(OrderLine, cascade=('all,delete'))
