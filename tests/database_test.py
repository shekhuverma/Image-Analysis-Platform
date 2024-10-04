import pytest

from src.db import services

# To store the UUID of the newly added image
shared_state = {"image_uuid": None, "create_user_id": None}


@pytest.mark.asyncio
async def test_create_user(create_user, db) -> None:
    user_id, created_user = await services.create_user(create_user, db)
    shared_state["create_user_id"] = user_id
    assert created_user.username == create_user.username


@pytest.mark.asyncio
async def test_get_user(create_user, db) -> None:
    created_user = await services.get_user(create_user.username, db)
    assert created_user.username == create_user.username


@pytest.mark.asyncio
async def test_upload_image(upload_image_db, db) -> None:
    upload_image_db.user_id = shared_state["create_user_id"]
    uploaded_image = await services.upload_image(upload_image_db, db)
    assert uploaded_image.user_id == upload_image_db.user_id
    assert uploaded_image.width == upload_image_db.width
    shared_state["image_uuid"] = uploaded_image.id


@pytest.mark.asyncio
async def test_get_image(upload_image_db, db) -> None:
    result = await services.get_image(shared_state["image_uuid"], db)
    upload_image_db.user_id = shared_state["create_user_id"]
    assert result.user_id == upload_image_db.user_id
    assert result.upload_date == upload_image_db.upload_date
    assert result.last_modified == upload_image_db.last_modified


@pytest.mark.asyncio
async def test_get_images(db) -> None:
    result = await services.get_images(shared_state["create_user_id"], db)
    assert result["total"] >= 1


@pytest.mark.asyncio
async def test_update_image(edit_image, db) -> None:
    original_image = await services.get_image(shared_state["image_uuid"], db)
    updated_image = await services.update_image(original_image, edit_image, db)
    assert updated_image.original_filename == edit_image.original_filename
    assert updated_image.width == edit_image.width


@pytest.mark.asyncio
async def test_delete_image(db) -> None:
    original_image = await services.get_image(shared_state["image_uuid"], db)
    await services.delete_image(original_image, db)
    assert await services.get_image(shared_state["image_uuid"], db) is None
