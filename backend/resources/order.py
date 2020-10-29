import collections
from typing import List

from fastapi import HTTPException
from fastapi_utils.cbv import cbv
from fastapi_utils.inferring_router import InferringRouter
from sqlalchemy import orm

from resources._base import BaseLoggedInResource
import schemas
import models
from const import OrderStatusValues, ORDER_STATUS_VALUES_NEXT

router = InferringRouter()


@cbv(router)
class OrderResource(BaseLoggedInResource):
    @router.get("/orders", response_model=List[schemas.Order])
    async def get(self):
        orders = self.db.query(models.Order)
        if self.user.is_owner:
            myrestaurants = self.db.query(models.Restaurant).filter(
                models.Restaurant.owner_id == self.user.id)
            orders = orders.filter(models.Order.restaurant_id.in_(
                [r.id for r in myrestaurants]))
        else:
            orders = orders.filter(models.Order.user_id == self.user.id)

        return orders.all()

    @router.post("/order", response_model=schemas.Order)
    async def create(self, data: schemas.OrderCreate):
        order = models.Order(
            restaurant_id=data.restaurant_id, user_id=self.user.id)
        self.db.add(order)
        self.db.commit()
        self.db.refresh(order)

        cnt = collections.Counter(data.meal_ids)
        for meal_id in cnt.keys():
            order_line = models.OrderLine(
                meal_id=meal_id, order_id=order.id, quantity=cnt[meal_id])
            self.db.add(order_line)

        history = models.OrderHistory(
            order_id=order.id, status=OrderStatusValues.PLACED)
        self.db.add(history)
        self.db.commit()
        self.db.refresh(order)

        return order

    @router.post("/order/ban")
    async def update_ban(self, data: schemas.OrderBan):
        await self.verify_is_owner()

        user = self.db.query(models.User).get(data.user_id)
        if user is None:
            raise HTTPException(status_code=403,
                                detail="User does not exist")
        if user.is_ban:
            raise HTTPException(status_code=403,
                                detail="User already banned")
        if user.is_owner:
            raise HTTPException(status_code=403,
                                detail="You can not ban another "
                                "restaurant owner")

        user.is_ban = True
        self.db.commit()

        return {}

    @router.put("/order/history", response_model=schemas.Order)
    async def update_history(self, data: schemas.OrderHistoryUpdate):
        # Let's get the order
        order = self._get_one(data.order_id)
        history = sorted(
            order.history, key=lambda x: x.updated_on, reverse=True)
        order_status = history[0]

        # Check who's sending
        if order.restaurant.owner_id == self.user.id:
            # Owner of the restaurant is updating the status
            if order_status.status in ORDER_STATUS_VALUES_NEXT['owner']:
                stakeholder = 'owner'
            else:
                # This shouldn't happen
                raise HTTPException(status_code=403,
                                    detail="Invalid value in Order History")
        elif order.user_id == self.user.id:
            if order_status.status in ORDER_STATUS_VALUES_NEXT['user']:
                stakeholder = 'user'
            else:
                # This shouldn't happen
                raise HTTPException(status_code=403,
                                    detail="Invalid value in Order History")
        else:
            # This shouldn't happen
            detail = "You are not the owner of the order/restaurant"
            raise HTTPException(status_code=403,
                                detail=detail)

        # Check the new requested status
        status = ORDER_STATUS_VALUES_NEXT[stakeholder][order_status.status]
        if data.status != status:
            # This shouldn't happen
            detail = "You can not change the order status to %s,"\
                " but only to %s" % (data.status, status)
            raise HTTPException(status_code=403,
                                detail=detail)

        # All clear
        history = models.OrderHistory(order_id=order.id,
                                      status=status)
        self.db.add(history)
        self.db.commit()
        self.db.refresh(order)

        return order

    def _get_one(self, id: int):
        try:
            order = self.db.query(models.Order).filter(
                models.Order.id == id).one()
        except orm.exc.MultipleResultsFound:
            # This really shouldn't happen because of the unique constrain
            raise HTTPException(status_code=403,
                                detail="Multiple order IDs with same value.")
        except orm.exc.NoResultFound:
            raise HTTPException(status_code=403,
                                detail="Invalid order ID.")
        else:
            return order
