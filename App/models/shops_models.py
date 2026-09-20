from pydantic import BaseModel, Field, ConfigDict
from typing import Annotated


class ShopBaseModel(BaseModel):
    address: str

    model_config = ConfigDict(from_attributes=True)


class ShopPostModel(ShopBaseModel):
    ...


class ShopGetModel(ShopBaseModel):
    id: int