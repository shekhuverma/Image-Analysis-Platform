from uuid import UUID

from sqlalchemy.orm import Session

from src.db import database, model
from src.schemas import image, user
from src.security.utils import get_password_hash


def save_db():
    session = database.SessionLocal()
    try:
        yield session
    finally:
        session.close()


def create_table():
    return database.Base.metadata.create_all(bind=database.engine)


async def upload_image(
    image_metadata: image.UploadImage, db: Session
) -> image.ImageinDB:
    added_image = model.Images(**image_metadata.model_dump())
    db.add(added_image)
    db.commit()
    db.refresh(added_image)
    return image.ImageinDB.model_validate(added_image)


async def get_image(image_id: UUID, db: Session) -> model.Images:
    image_metadata = db.query(model.Images).filter(model.Images.id == image_id).first()
    return image_metadata


async def get_images(
    user_id: int,
    db: Session,
    skip: int = 1,
    limit: int = 20,
):
    # if we don't do -1 then it will skip the first row everytime
    start = (skip - 1) * limit

    images = db.query(model.Images).filter(model.Images.user_id == user_id)
    images_count = images.count()
    images = images.offset(start).limit(limit).all()
    return {
        "total": images_count,
        "data": images,
    }


async def update_image(
    image_metadata: model.Images, edit_image: image.EditImage, db: Session
) -> image.ImageinDB:
    for key, value in edit_image.model_dump(exclude_unset=True).items():
        setattr(image_metadata, key, value)

    setattr(image_metadata, "last_modified", edit_image.last_modified)
    db.add(image_metadata)
    db.commit()
    db.refresh(image_metadata)
    return image.ImageinDB.model_validate(image_metadata)


async def delete_image(image_instance: model.Images, db: Session):
    db.delete(image_instance)
    db.commit()


async def create_user(
    user_data: user.CreateUser, db: Session
) -> tuple[int, user.UserInDB]:
    created_user = user.UserInDB(
        **user_data.model_dump(),
        hashed_password=get_password_hash(user_data.password),
    )
    created_user = model.Users(**created_user.model_dump())
    db.add(created_user)
    db.commit()
    db.refresh(created_user)
    return created_user.id, user.UserInDB.model_validate(created_user)


async def get_user(username: str, db: Session):
    user = db.query(model.Users).filter(model.Users.username == username).first()
    return user
