from pydantic import BaseModel, Field, ConfigDict, computed_field
from typing import Annotated
from ..utils import PasswordManager


class UserBaseModel(BaseModel):
    username: Annotated[str, Field(max_length=100)]

    model_config = ConfigDict(
        from_attributes=True,
        validate_by_alias=True,
        serialize_by_alias=True,
    )


class UserPostModel(UserBaseModel):
    plain_password: Annotated[str, Field(max_length=72, alias="plainPassword", exclude=True)]

    @computed_field("hash_password")
    def hash_password(self) -> str:
        return PasswordManager.hash_password(self.plain_password)


class UserLoginModel(UserBaseModel):
    plain_password: Annotated[str, Field(max_length=72, alias="plainPassword", exclude=True)]




class UserGetModel(UserBaseModel):
    id: int
    password_hash: Annotated[str, Field(alias="passwordHash")]
    is_admin: Annotated[bool, Field(alias="isAdmin")]
    is_blocked: Annotated[bool, Field(alias="isBlocked")]



class UserSingleModel(UserBaseModel):
    id: int
   