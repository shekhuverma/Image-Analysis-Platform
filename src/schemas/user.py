from pydantic import BaseModel, ConfigDict, EmailStr


class User(BaseModel):
    username: str
    email: EmailStr
    disabled: bool | None = False


# To create new admin
class CreateUser(User):
    password: str


# To store admin in the database
class UserInDB(User):
    hashed_password: str
    model_config = ConfigDict(from_attributes=True)
