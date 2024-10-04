import httpx
import pytest

from src.main import app

app = httpx.ASGITransport(app=app)


@pytest.mark.asyncio(scope="session")
async def test_login(login_credentials, db) -> None:
    async with httpx.AsyncClient(
        transport=app, base_url="http://localhost:8000"
    ) as client:
        response = await client.post(
            "/login",
            data=login_credentials,
        )
    assert response.status_code == 200
    token = response.json()["access_token"]
    assert token is not None


# @pytest.mark.asyncio(scope="session")
# async def test_signup(create_user, db) -> None:
#     async with httpx.AsyncClient(
#         transport=app, base_url="http://localhost:8000"
#     ) as client:
#         response = await client.post(
#             "/signup",
#             content=create_user.model_dump_json(),
#         )
#     get_user = await services.get_user(username=create_user.username, db=db)
#     assert response.status_code == 200
#     assert create_user.username == get_user.username
#     assert create_user.email == get_user.email


@pytest.mark.asyncio(scope="session")
async def test_signup_same_username(create_user, db) -> None:
    async with httpx.AsyncClient(
        transport=app, base_url="http://localhost:8000"
    ) as client:
        response = await client.post(
            "/signup",
            content=create_user.model_dump_json(),
        )
    assert response.status_code == 400
