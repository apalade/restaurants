from typing import Optional, List
from fastapi import HTTPException
from fastapi_utils.cbv import cbv
from fastapi_utils.inferring_router import InferringRouter
from sqlalchemy import orm

from resources._base import BaseLoggedInResource
import schemas
import models

router = InferringRouter()


@cbv(router)
class RestaurantResource(BaseLoggedInResource):
    @router.get("/restaurants", response_model=List[schemas.Restaurant])
    async def get(self, owner_id: Optional[int] = None):
        restaurants = self.db.query(models.Restaurant).\
            filter(models.Restaurant.deleted.is_(False))

        if owner_id is not None:
            restaurants = restaurants.filter(
                models.Restaurant.owner_id == owner_id)
        
        return restaurants.all()

    @router.post("/restaurant", response_model=schemas.Restaurant)
    async def create(self, data: schemas.RestaurantCreate):
        await self.verify_is_owner()

        params = data.dict()
        params['owner_id'] = self.user.id
        restaurant = models.Restaurant(**params)
        self.db.add(restaurant)
        self.db.commit()
        self.db.refresh(restaurant)

        return restaurant

    @router.put("/restaurant", response_model=schemas.Restaurant)
    async def update(self, data: schemas.RestaurantUpdate):
        await self.verify_is_owner()

        restaurant = self._get_one(data.id)
        if restaurant.owner_id != self.user.id:
            raise HTTPException(status_code=403,
                                detail="You do not have access to"
                                "edit this restaurant.")

        restaurant.name = data.name
        restaurant.description = data.description
        self.db.commit()
        self.db.refresh(restaurant)

        return restaurant

    @router.delete("/restaurant")
    async def delete(self, rid: int):
        await self.verify_is_owner()

        restaurant = self._get_one(rid)
        if restaurant.owner_id != self.user.id:
            raise HTTPException(status_code=403,
                                detail="You do not have access"
                                " to delete this restaurant.")

        restaurant.deleted = True
        #self.db.delete(restaurant)
        self.db.commit()

    def _get_one(self, id: int):
        try:
            restaurant = self.db.query(models.Restaurant).filter(
                models.Restaurant.id == id).one()
        except orm.exc.MultipleResultsFound:
            # This really shouldn't happen because of the unique constrain
            raise HTTPException(status_code=403,
                                detail="Multiple restaurant IDs "
                                "with same value.")
        except orm.exc.NoResultFound:
            raise HTTPException(status_code=403,
                                detail="Invalid restaurant ID.")
        else:
            return restaurant
