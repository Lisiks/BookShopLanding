from pydantic import BaseModel, Field, ConfigDict
from typing import Annotated


class ShopBaseModel(BaseModel):
    phone: Annotated[str, Field(pattern="^\\+\\d{1,3}\\(\\d{3}\\)\\d{3}-\\d{2}-\\d{2}$")]

    town: Annotated[str, Field(max_length=100)]
    street: Annotated[str, Field(max_length=100)]
    housing: Annotated[str, Field(pattern="^[1-9]{1,5}?\\w$")]

    model_config = ConfigDict(from_attributes=True)


class ShopPostModel(ShopBaseModel):
    ...


class ShopGetModel(ShopBaseModel):
    id: int