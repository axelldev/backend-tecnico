from fastapi import status
from fastapi.testclient import TestClient
from bson.objectid import ObjectId
from pymongo.collection import Collection
from pytest import fixture
from app.config import database
from app.main import app


@fixture(scope="module")
def test_client():
    client = TestClient(app)
    yield client


@fixture(scope="module")
def db():
    yield database.users_collection
    database.client.drop_database(database.db)


def test_list_users(test_client: TestClient, db: Collection):
    """Test the list of users"""
    payload = [
        {
            "first_name": "Karla",
            "last_name": "Hurtado",
            "email": "karla@gmail.com",
            "phone": 5542771463,
            "password": "pass1234",
        },
        {
            "first_name": "Axell",
            "last_name": "Solis",
            "email": "axell@gmail.com",
            "phone": 5542771463,
            "password": "pass1234",
        },
    ]

    db.insert_many(payload)
    response = test_client.get("/users")

    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()) == 2


def test_create_user(test_client: TestClient, db: Collection):
    """Test to post a user creates on database an returns it."""
    payload = {
        "first_name": "Joaquin",
        "last_name": "Rubio",
        "email": "juan@gmail.com",
        "phone": 5542771463,
        "password": "pass1234",
    }

    response = test_client.post("/users", json=payload)
    assert response.status_code == status.HTTP_201_CREATED

    data = response.json()
    entity = db.find_one({"_id": ObjectId(data["id"])})

    assert entity is not None


def test_detail_user(test_client: TestClient, db: Collection):
    """Tests returns the user data by email"""
    payload = {
        "first_name": "Some",
        "last_name": "User",
        "email": "test_email@example.com",
        "phone": 5542771463,
        "password": "test1234",
    }
    inserted_id = db.insert_one(payload).inserted_id
    entity = db.find_one({"_id": inserted_id})

    email = payload["email"]
    response = test_client.get(f"/users/{email}")
    data = response.json()

    assert response.status_code == status.HTTP_200_OK
    assert data["email"] == payload["email"]
    assert str(entity["_id"]) == data["id"]
