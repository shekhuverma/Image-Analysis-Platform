import json
from typing import Annotated
from uuid import UUID

import redis
from fastapi import APIRouter, Depends, Security
from fastapi.exceptions import HTTPException

from src.db import services
from src.schemas.image import EditImage, ImageinDB, ImageMetaData, UploadImage
from src.security.security import get_current_active_user
from src.settings import REDIS_EXPIRY, config

rd = redis.Redis(host=config.REDIS_HOST, port=6379, db=0)


router = APIRouter(prefix="/image", tags=["Images"])


@router.get("/{image_id}")
async def image_details(
    image_id: UUID,
    current_user: Annotated[
        any,
        Security(get_current_active_user),
    ],
    db: Annotated[any, Depends(services.save_db)],
):
    """
    Get image metadata

    - **Arguments:**
        - image_id -- Image UUID

    - **Raises:**
        - HTTPException: 404 if the image doesn't exist
        - HTTPException: 403 if the image does not belong to the user

    - **Returns:** ImageinDB instance
    """
    # first checking for data in cache
    image_metadata = rd.get(str(image_id))

    if image_metadata:
        image_metadata = ImageinDB(**json.loads(image_metadata))
    else:
        image_metadata = await services.get_image(image_id, db)

        if image_metadata is None:
            raise HTTPException(404, detail="Resource not found!")

        # Adding the data to cache
        image_metadata = ImageinDB.model_validate(image_metadata)
        rd.set(str(image_id), image_metadata.model_dump_json(), REDIS_EXPIRY)

    if current_user.id == image_metadata.user_id:
        return image_metadata
    raise HTTPException(403, detail="This image does not belong to you!")


@router.get("/all")
async def all_images(
    current_user: Annotated[
        any,
        Security(get_current_active_user),
    ],
    db: Annotated[any, Depends(services.save_db)],
    # For pagination
    skip: int = 1,  # Page Number
    limit: int = 20,  # Page Size
):
    """
    Returns all the images from a user
    - **Returns:** {
                    "total": Image_count
                    "data": [images_Metadata],
                    }

    """
    print("shekhar")
    return await services.get_images(current_user.id, skip, limit, db)


@router.delete("/{image_id}")
async def delete_image(
    image_id: UUID,
    current_user: Annotated[
        any,
        Security(get_current_active_user),
    ],
    db: Annotated[any, Depends(services.save_db)],
):
    """
    Deletes the image

    - **Arguments:**
        - image_id -- Image UUID

    - **Raises:**
        - HTTPException: 404 if the image doesn't exist
        - HTTPException: 403 if the image does not belong to the user

    - **Returns:** None
    """
    # Checking if the image exist and belongs to user
    image_metadata = await image_details(image_id, current_user, db)
    if image_metadata:
        # Deleting the data from cache
        rd.delete(str(image_id))

        await services.delete_image(image_metadata, db)

        # Delete the image form file storage as well(For ex- AWS S3)
        # Dummy_s3_delete_function()


@router.put("/{image_id}")
async def edit_image(
    image_id: UUID,
    edit_metadata: EditImage,
    db: Annotated[any, Depends(services.save_db)],
    current_user: Annotated[
        any,
        Security(get_current_active_user),
    ],
):
    # Checking if the image exist and belongs to user
    image_metadata = await image_details(image_id, current_user, db)
    if image_metadata:
        return await services.update_image(image_metadata, edit_metadata, db)
    return None


@router.post("/upload")
async def upload_image(
    current_user: Annotated[
        any,
        Security(get_current_active_user),
    ],
    image_metadata: ImageMetaData,
    db: Annotated[any, Depends(services.save_db)],
    # image: Optional[UploadFile] = None,  # Keeping file upload optional for now
):
    """
    Upload the image
    """
    # if image:
    #     image_extension = image.filename.split(".")[
    #         -1
    #     ]  # Getting the uploaded image format

    #     if image_extension.lower() not in SUPPORTED_FILE_FORMATS:
    #         raise HTTPException(
    #             400,
    #             detail=f"File with extension {image_extension} is invalid.Only {SUPPORTED_FILE_FORMATS} are supported for now.",
    #         )

    image_metadata = UploadImage(user_id=current_user.id, **image_metadata.model_dump())
    return await services.upload_image(image_metadata, db)


@router.get("/download/{image_id}")
async def download_image(
    image_id: UUID,
    db: Annotated[any, Depends(services.save_db)],
    current_user: Annotated[
        any,
        Security(get_current_active_user),
    ],
):
    """
    Downloads the image

    - **Arguments:**
        - image_id -- Image UUID

    - **Raises:**
        - HTTPException: 404 if the image doesn't exist
        - HTTPException: 403 if the image does not belong to the user

    - **Returns:** Image file
    """
    # Checking if the image exist and belongs to user
    image_metadata = await image_details(image_id, current_user, db)
    if image_metadata:
        return True
        # return dummy_function_to_get_download_link_from_s3()
    return None
