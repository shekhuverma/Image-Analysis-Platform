import pytest
from fastapi.testclient import TestClient

from src.db import database
from src.main import app
from src.schemas import image, user
from src.settings import config

client = TestClient(app)


@pytest.fixture(scope="session")
def db():
    return database.SessionLocal()


@pytest.fixture(scope="session")
def create_user():
    return user.CreateUser(
        username="testing",
        email="testing@example.com",
        password="testing",
    )


@pytest.fixture(scope="session")
def image_metadata():
    return image.Image(
        original_filename="image.jpeg",
        height=100,
        width=100,
        file_type="jpeg",
        file_size=100,
    )


@pytest.fixture(scope="session")
def upload_image_db():
    return image.UploadImage(
        user_id=9999,
        original_filename="image_db.jpeg",
        height=100,
        width=100,
        file_type="jpeg",
        file_size=100,
    )


@pytest.fixture(scope="session")
def edit_image():
    return image.EditImage(
        original_filename="image_modified.jpeg",
        width=200,
    )


@pytest.fixture(scope="session")
def login_credentials():
    return {
        "username": config.BASEUSER,
        "password": config.BASEUSER_PASSWORD,
    }


# Fixture to test secured endpoints
@pytest.fixture(scope="session")
def login(login_credentials):
    response = client.post("/login", data=login_credentials)
    assert response.status_code == 200
    token = response.json()["access_token"]
    assert token is not None
    return token


# Fixture to test resource access
# For example this will successfully signup but will  not be able to access
# the resources of other users
@pytest.fixture(scope="session")
def login_another_user():
    response = client.post(
        "/login",
        data={
            "username": "testing",
            "password": "testing",
        },
    )
    assert response.status_code == 200
    token = response.json()["access_token"]
    assert token is not None
    return token
