import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class Image(BaseModel):
    original_filename: str
    height: int
    width: int
    file_type: str
    file_size: int
    model_config = ConfigDict(from_attributes=True)


# Just to improve readibility
class ImageMetaData(Image):
    pass


class UploadImage(Image):
    user_id: int
    upload_date: datetime.datetime = datetime.datetime.now(tz=datetime.UTC)
    last_modified: datetime.datetime = datetime.datetime.now(tz=datetime.UTC)
    model_config = ConfigDict(from_attributes=True)


class ImageinDB(UploadImage):
    id: UUID
    model_config = ConfigDict(from_attributes=True)


class EditImage(BaseModel):
    original_filename: Optional[str] = None
    height: Optional[int] = None
    width: Optional[int] = None
    file_type: Optional[str] = None
    file_size: Optional[int] = None
    last_modified: datetime.datetime = datetime.datetime.now(tz=datetime.UTC)
    model_config = ConfigDict(from_attributes=True)
