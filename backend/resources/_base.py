from fastapi import Depends, Header, HTTPException
from sqlalchemy.orm import Session, exc

from database import get_db
import models


async def get_user(x_token: str = Header(...),
                   x_user: int = Header(...),
                   db: Session = Depends(get_db)):

    try:
        user = db.query(models.User).\
            filter(models.User.id == x_user).\
            filter(models.User.token == x_token).\
            filter(models.User.is_ban.is_(False)).one()
    except exc.MultipleResultsFound:
        # Should not happen
        raise HTTPException(
            status_code=403, detail="Multiple results found.")
    except exc.NoResultFound:
        raise HTTPException(
            status_code=403, detail="Wrong/expired user/token.")
    else:
        return user


class BaseResource(object):
    db: Session = Depends(get_db)


class BaseLoggedInResource(BaseResource):
    user: models.User = Depends(get_user)

    async def verify_is_owner(self):
        if not self.user.is_owner:
            raise HTTPException(
                status_code=403, detail="Only owners are allowed.")
