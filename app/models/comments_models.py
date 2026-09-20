from pydantic import BaseModel, Field, ConfigDict
from typing import Annotated
from datetime import datetime

from .users_models import UserSingleModel

class CommentBaseModel(BaseModel):

    book_id: Annotated[int, Field(alias="bookId")]
    user_id: Annotated[int, Field(alias="userId")]
    text: str

    model_config = ConfigDict(
        from_attributes=True,
        validate_by_alias=True,
        serialize_by_alias=True,
        extra="ignore"
    )


class CommentPostModel(CommentBaseModel):
    ...


class CommentGetModel(CommentBaseModel):
    datetime: datetime
    user: UserSingleModel
