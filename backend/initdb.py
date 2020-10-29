import hashlib

import factory

import models
from database import SessionLocal, engine

session = SessionLocal()


class UserFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = models.User
        sqlalchemy_session = session   # the SQLAlchemy session object

    id = factory.Sequence(lambda n: n)
    email = factory.Sequence(lambda n: u'u%d@gmail.com' % n)
    password = hashlib.md5(b'123').hexdigest()
    is_owner = True


class RestaurantFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = models.Restaurant
        sqlalchemy_session = session   # the SQLAlchemy session object

    id = factory.Sequence(lambda n: n)
    name = factory.Sequence(lambda n: u'Restaurant %d' % n)
    description = factory.Sequence(lambda n: u'Restaurant %d description ' % n)


class MealFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = models.Meal
        sqlalchemy_session = session   # the SQLAlchemy session object

    id = factory.Sequence(lambda n: n)
    name = factory.Sequence(lambda n: u'Meal %d' % n)
    description = factory.Sequence(lambda n: u'Meal %d description ' % n)
    price = factory.Sequence(lambda n: n)


models.Base.metadata.drop_all(bind=engine)
models.Base.metadata.create_all(bind=engine)

UserFactory()
UserFactory()
user = UserFactory()
UserFactory(is_owner=False)
r0 = RestaurantFactory(owner_id=user.id)
r1 = RestaurantFactory(owner_id=user.id)
r2 = restaurant = RestaurantFactory(owner_id=user.id)
MealFactory(restaurant_id=r0.id)
MealFactory(restaurant_id=r1.id)
MealFactory(restaurant_id=r2.id)
session.commit()
