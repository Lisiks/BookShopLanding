from pydantic import BaseModel, Field, field_validator
from typing import Annotated


class ShopingCartDTO(BaseModel):
    items: Annotated[list[int], Field(max_length=10, alias="items")]

    @field_validator("items", mode="after")
    @classmethod
    def validate_items_unique(cls, value: list[int]) -> list[int]:
        if len(value) != len(set(value)):
            raise ValueError("Items list contains recurring positions!")

        return value


