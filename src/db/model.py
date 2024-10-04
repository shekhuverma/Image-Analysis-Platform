import uuid

from sqlalchemy import UUID, Boolean, Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from src.db.database import Base


# Refer to README.md for more details
class Users(Base):
    __tablename__ = "users"
    id = Column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )
    username = Column(String, unique=True, index=True)
    email = Column(String, index=True)
    disabled = Column(Boolean, default=False)
    hashed_password = Column(String)

    images = relationship("Images", back_populates="user")


class Images(Base):
    __tablename__ = "images"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(ForeignKey("users.id", ondelete="CASCADE"))
    original_filename = Column(String)
    width = Column(Integer)
    height = Column(Integer)
    file_size = Column(Integer)
    file_type = Column(String)
    upload_date = Column(DateTime(timezone=True))
    last_modified = Column(DateTime(timezone=True))

    user = relationship("Users", back_populates="images")
