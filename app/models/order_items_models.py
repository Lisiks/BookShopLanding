from pydantic import BaseModel, Field, ConfigDict
from typing import Annotated


class OrderItemBaseModel(BaseModel):
    book_id: Annotated[int, Field(alias="bookId")]
    count: Annotated[int, Field(gt=0)]

    model_config = ConfigDict(
        from_attributes=True,
        validate_by_alias=True,
        serialize_by_alias=True,
        extra="ignore"
    )