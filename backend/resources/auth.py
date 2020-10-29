import datetime
import hashlib

from fastapi import HTTPException
from fastapi_utils.cbv import cbv
from fastapi_utils.inferring_router import InferringRouter
from sqlalchemy import orm, exc

from resources._base import BaseResource
import schemas
import models

router = InferringRouter()


@cbv(router)
class AuthResource(BaseResource):
    @router.post("/auth/login", response_model=schemas.User)
    async def login(self, data: schemas.UserLogin):
        email = data.email
        password = data.password
        hex = hashlib.md5(password.encode('utf-8')).hexdigest()
        user = self._get_user_by_password(email, hex)
        if user is None:
            raise HTTPException(status_code=403,
                                detail="Wrong email/password")
        if user.is_ban:
            raise HTTPException(status_code=403,
                                detail="User has been banned.")

        seed = email + password + datetime.datetime.utcnow().isoformat()
        token = hashlib.md5(seed.encode('utf-8')).hexdigest()
        token_valid_until = datetime.datetime.utcnow() + \
            datetime.timedelta(hours=12)

        # Update the database value
        user.token = token
        user.token_valid_until = token_valid_until
        self.db.commit()
        self.db.refresh(user)

        return user

    @router.post("/auth/register", response_model=schemas.User)
    async def register(self, data: schemas.UserCreate, ):
        hex = hashlib.md5(data.password.encode('utf-8')).hexdigest()
        user = models.User(email=data.email, password=hex,
                           is_owner=data.is_owner)
        self.db.add(user)
        try:
            self.db.commit()
        except exc.IntegrityError:
            raise HTTPException(status_code=403,
                                detail="Email already exists.")
        self.db.refresh(user)

        return user

    def _get_user_by_password(self, email: str, password: str):
        try:
            db_user = self.db.query(models.User).\
                filter(models.User.email == email).\
                filter(models.User.password == password).one()
        except orm.exc.MultipleResultsFound:
            return None
        except orm.exc.NoResultFound:
            return None
        else:
            return db_user
