import pytest

from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database import Base, get_db
from main import app

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False},
)
TestingSessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=engine)
Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)


def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db
client = TestClient(app)


@pytest.fixture(scope="module", autouse=True)
def headers():
    headers = {}

    data = {
        'email': 'test@gmail.com',
        'password': '12345',
        'is_owner': False,
    }
    response = client.post("/auth/register", json=data)
    response = client.post("/auth/login", json=data)
    r = response.json()
    assert response.status_code == 200
    headers['user'] = {
        'X-token': r['token'],
        'X-user': str(r['id'])
    }

    data = {
        'email': 'test-owner@gmail.com',
        'password': '12345',
        'is_owner': True,
    }
    response = client.post("/auth/register", json=data)
    response = client.post("/auth/login", json=data)
    r = response.json()
    assert response.status_code == 200
    headers['owner'] = {
        'X-token': r['token'],
        'X-user': str(r['id'])
    }
    yield headers


def test_main():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello World"}


def test_auth():
    # Empty fields not allowed
    data = {
        'email': '',
        'password': '',
        'is_owner': True,
    }
    response = client.post("/auth/register", json=data)
    assert response.status_code == 422

    data = {
        'email': 'alex@loopback.ro',
        'password': '12345',
        'is_owner': True,
    }
    response = client.post("/auth/register", json=data)
    assert response.status_code == 200

    # Duplicate email not allowed
    response = client.post("/auth/register", json=data)
    assert response.status_code != 200

    # Test login
    new_data = data.copy()
    del new_data['is_owner']
    response = client.post("/auth/login", json=new_data)
    r = response.json()
    assert response.status_code == 200
    assert r['email'] == data['email']
    assert r['is_owner'] == data['is_owner']
    assert r['token']


def test_restaurant(headers):
    response = client.get("/restaurants", headers=headers['user'])
    assert response.status_code == 200
    assert response.json() == []

    data = {
        'name': 'Rest',
        'description': 'Desc'
    }

    # POST
    response = client.post("/restaurant", json=data, headers=headers['user'])
    assert response.status_code == 403

    response = client.post("/restaurant", json=data, headers=headers['owner'])
    assert response.status_code == 200
    data_commited = response.json()
    assert data_commited['name'] == data['name']
    assert data_commited['description'] == data['description']
    assert 'id' in data_commited

    # PUT
    data_commited['name'] = 'New Rest'
    response = client.put("/restaurant", json=data_commited,
                          headers=headers['owner'])
    assert response.status_code == 200
    data_commited_2 = response.json()
    assert data_commited_2['name'] != data['name']
    assert data_commited_2['name'] == data_commited['name']
    assert data_commited_2['description'] == data_commited['description']
    assert 'id' in data_commited_2

    # GET
    response = client.get("/restaurants", headers=headers['user'])
    assert response.status_code == 200
    r = response.json()
    assert len(r) == 1
    assert r[0]['name'] == data_commited_2['name']
    assert r[0]['description'] == data_commited_2['description']
    assert r[0]['id'] == data_commited_2['id']
    assert r[0]['owner_id'] == data_commited_2['owner_id']

    response = client.get(
        "/restaurants",
        params={'owner_id': data_commited_2['owner_id']},
        headers=headers['user'])
    assert response.status_code == 200
    r = response.json()
    assert len(r) == 1
    assert r[0]['name'] == data_commited_2['name']
    assert r[0]['description'] == data_commited_2['description']
    assert r[0]['id'] == data_commited_2['id']
    assert r[0]['owner_id'] == data_commited_2['owner_id']

    response = client.get(
        "/restaurants", params={'owner_id': 1233455}, headers=headers['user'])
    assert response.status_code == 200
    r = response.json()
    assert len(r) == 0

    # DELETE
    response = client.delete(
        "/restaurant",
        params={'rid': data_commited_2['id']},
        headers=headers['user'])
    assert response.status_code == 403
    response = client.delete(
        "/restaurant", params={'rid': 321321}, headers=headers['owner'])
    assert int(response.status_code) == 403
    response = client.delete(
        "/restaurant", params={'rid': data_commited_2['id']},
        headers=headers['owner'])
    assert response.status_code == 200
    response = client.get("/restaurants", headers=headers['user'])
    assert response.status_code == 200
    r = response.json()
    assert len(r) == 0


def test_meals(headers):
    response = client.get("/meals", headers=headers['user'])
    assert response.status_code == 200
    assert response.json() == []

    # Create a restaurant
    restaurant = _create_restaurant(headers)

    # POST
    data = {
        'name': 'Meal',
        'description': 'Description for meal',
        'price': 2.3,
        'restaurant_id': restaurant['id']
    }
    response = client.post("/meal", json=data, headers=headers['user'])
    assert response.status_code == 403

    response = client.post("/meal", json=data, headers=headers['owner'])
    assert response.status_code == 200
    data_commited = response.json()
    assert data['name'] == data_commited['name']
    assert data['description'] == data_commited['description']
    assert data['price'] == data_commited['price']
    assert data['restaurant_id'] == data_commited['restaurant']['id']

    # PUT
    data['name'] = 'New Meal'
    data['description'] = 'New Description'
    data['price'] = 1
    data['id'] = data_commited['id']
    response = client.put("/meal", json=data,
                          headers=headers['owner'])
    assert response.status_code == 200
    data_commited_2 = response.json()
    assert data_commited_2['name'] == data['name']
    assert data_commited_2['description'] == data['description']
    assert data_commited_2['price'] == data['price']
    assert data_commited_2['restaurant']['id'] == \
        data['restaurant_id']

    # GET
    response = client.get("/meals", headers=headers['user'])
    assert response.status_code == 200
    r = response.json()
    assert len(r) == 1
    assert r[0]['name'] == data_commited_2['name']
    assert r[0]['description'] == data_commited_2['description']
    assert r[0]['id'] == data_commited_2['id']
    assert r[0]['price'] == data_commited_2['price']
    assert r[0]['restaurant']['id'] == data_commited['restaurant']['id']

    response = client.get(
        "/meals", params={'owner_id': headers['user']['X-user']},
        headers=headers['user'])
    assert response.status_code == 200
    r = response.json()
    assert len(r) == 0
    response = client.get(
        "/meals", params={'owner_id': headers['owner']['X-user']},
        headers=headers['user'])
    assert response.status_code == 200
    r = response.json()
    assert len(r) == 1

    # DELETE
    response = client.delete(
        "/meal", params={'mid': data_commited_2['id']},
        headers=headers['user'])
    assert response.status_code == 403
    response = client.delete(
        "/meal", params={'mid': 321321},
        headers=headers['owner'])
    assert int(response.status_code) == 403
    response = client.delete(
        "/meal", params={'mid': data_commited_2['id']},
        headers=headers['owner'])
    assert response.status_code == 200
    response = client.get("/meals", headers=headers['user'])
    assert response.status_code == 200
    r = response.json()
    assert len(r) == 0


def test_orders(headers):
    response = client.get("/orders", headers=headers['user'])
    assert response.status_code == 200
    assert response.json() == []

    # Create a restaurant
    restaurant = _create_restaurant(headers)
    meal = _create_meal(headers, restaurant)
    meal2 = _create_meal(headers, restaurant)

    data = {
        'restaurant_id': restaurant['id'],
        'meal_ids': [meal['id'], meal2['id'], meal2['id']],
    }
    response = client.post("/order", json=data, headers=headers['user'])
    assert response.status_code == 200
    order = response.json()
    assert order['total'] == meal['price'] + meal2['price'] * 2

    data = {
        'order_id': order['id'],
        'status': 'Processing'
    }
    response = client.put("/order/history", json=data, headers=headers['user'])

    assert int(response.status_code) == 403
    data['status'] = 'Cancelled'
    response = client.put("/order/history", json=data,
                          headers=headers['owner'])
    assert int(response.status_code) == 403
    response = client.put("/order/history", json=data, headers=headers['user'])
    assert response.status_code == 200

    data = {
        'user_id': headers['user']['X-user']
    }
    response = client.post("/order/ban", json=data, headers=headers['user'])
    assert response.status_code == 403
    response = client.post("/order/ban", json=data, headers=headers['owner'])
    assert response.status_code == 200
    data = {
        'user_id': headers['owner']['X-user']
    }
    response = client.post("/order/ban", json=data, headers=headers['owner'])
    assert response.status_code == 403


def _create_restaurant(headers):
    data = {
        'name': 'Rest',
        'description': 'Desc'
    }
    response = client.post("/restaurant", json=data, headers=headers['owner'])
    restaurant = response.json()

    return restaurant


def _create_meal(headers, restaurant):

    data = {
        'name': 'Meal',
        'description': 'Description for meal',
        'price': 2.3,
        'restaurant_id': restaurant['id']
    }
    response = client.post("/meal", json=data, headers=headers['owner'])
    assert response.status_code == 200
    return response.json()
