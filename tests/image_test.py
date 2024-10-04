import httpx
import pytest

from src.db import services
from src.main import app
from src.schemas import image

app = httpx.ASGITransport(app=app)

# To store the UUID of the newly added image
shared_state = {"image_uuid": None}


@pytest.mark.asyncio(scope="session")
async def test_upload_image(image_metadata, login, db) -> None:
    async with httpx.AsyncClient(
        transport=app, base_url="http://localhost:8000/image"
    ) as client:
        response = await client.post(
            "/upload",
            content=image_metadata.model_dump_json(),
            headers={
                "Authorization": f"Bearer {login}",
                "Content-Type": "application/json",
                "accept": "application/json",
            },
        )
    result = response.json()
    shared_state["image_uuid"] = result["id"]
    get_user = await services.get_image(result["id"], db=db)
    assert response.status_code == 200
    assert get_user.original_filename == image_metadata.original_filename


@pytest.mark.asyncio(scope="session")
async def test_image_details(login, db) -> None:
    async with httpx.AsyncClient(
        transport=app, base_url="http://localhost:8000/image"
    ) as client:
        response = await client.get(
            f"/{shared_state["image_uuid"]}",
            headers={
                "Authorization": f"Bearer {login}",
                "Content-Type": "application/json",
                "accept": "application/json",
            },
        )
    print(shared_state["image_uuid"])
    assert response.status_code == 200
    result = image.ImageinDB(**response.json())
    get_user = await services.get_image(result.id, db=db)
    assert get_user.original_filename == result.original_filename


@pytest.mark.asyncio(scope="session")
async def test_image_details_anotherUser(login_another_user, db) -> None:
    async with httpx.AsyncClient(
        transport=app, base_url="http://localhost:8000/image"
    ) as client:
        response = await client.get(
            f"/{shared_state["image_uuid"]}",
            headers={
                "Authorization": f"Bearer {login_another_user}",
                "Content-Type": "application/json",
                "accept": "application/json",
            },
        )
    assert response.status_code == 403


# @pytest.mark.asyncio(scope="session")
# async def test_all_images(login, db) -> None:
#     async with httpx.AsyncClient(
#         transport=app, base_url="http://localhost:8000/image"
#     ) as client:
#         response = await client.get(
#             "/all",
#             headers={
#                 "Authorization": f"Bearer {login}",
#                 "Content-Type": "application/json",
#                 "accept": "application/json",
#             },
#         )
#     assert response.status_code == 200
