from typing import List, Optional
from fastapi import HTTPException
from fastapi_utils.cbv import cbv
from fastapi_utils.inferring_router import InferringRouter
from sqlalchemy import orm

from resources._base import BaseLoggedInResource
import schemas
import models

router = InferringRouter()


@cbv(router)
class MealResource(BaseLoggedInResource):
    @router.get("/meals", response_model=List[schemas.Meal])
    async def get(self, owner_id: Optional[int] = None):
        meals = self.db.query(models.Meal)
        if owner_id is not None:
            meals = meals.join(models.Restaurant).\
                filter(models.Restaurant.owner_id == owner_id)
        return meals.all()

    @router.post("/meal", response_model=schemas.Meal)
    async def create(self, data: schemas.MealCreate):
        await self.verify_is_owner()

        restaurant = self.db.query(models.Restaurant).get(data.restaurant_id)
        if restaurant is None:
            raise HTTPException(status_code=403,
                                detail="Invalid restaurant ID.")

        params = data.dict()
        meal = models.Meal(**params)
        self.db.add(meal)
        self.db.commit()
        self.db.refresh(meal)

        return meal

    @router.put("/meal", response_model=schemas.Meal)
    async def update(self, data: schemas.MealUpdate):
        await self.verify_is_owner()

        restaurant = self.db.query(models.Restaurant).get(data.restaurant_id)
        if restaurant is None:
            detail = "Invalid restaurant ID."
            raise HTTPException(status_code=403,
                                detail=detail)

        if restaurant.owner_id != self.user.id:
            detail = "You do not have access to edit this meal."
            raise HTTPException(status_code=403,
                                detail=detail)

        meal = self._get_one(data.id)
        meal.name = data.name
        meal.description = data.description
        meal.price = data.price
        meal.restaurant_id = data.restaurant_id

        self.db.commit()
        self.db.refresh(meal)

        return meal

    @router.delete("/meal")
    async def delete(self, mid: int):
        await self.verify_is_owner()

        meal = self._get_one(mid)
        if meal.restaurant.owner_id != self.user.id:
            detail = "You do not have access to delete this meal."
            raise HTTPException(status_code=403,
                                detail=detail)

        self.db.delete(meal)
        self.db.commit()

    def _get_one(self, id: int):
        try:
            meal = self.db.query(models.Meal).filter(
                models.Meal.id == id).one()
        except orm.exc.MultipleResultsFound:
            # This really shouldn't happen because of the unique constrain
            raise HTTPException(status_code=403,
                                detail="Multiple meal IDs with same value.")
        except orm.exc.NoResultFound:
            raise HTTPException(status_code=403,
                                detail="Invalid meal ID.")
        else:
            return meal
