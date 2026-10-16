from pydantic import BaseModel, Field, ConfigDict, field_validator
from typing import Annotated
from datetime import datetime

from .order_items_models import OrderItemsGetModel, OrderItemsPostModel
from .shops_models import ShopGetModel
from .users_models import UserGetModel
from ..enums import OrderStatuses


class OrderBaseModel(BaseModel):
    shop_id: Annotated[int, Field(gt=0, alias="shopId")]

    model_config = ConfigDict(
        from_attributes=True,
        validate_by_alias=True,
        serialize_by_alias=True
    )


class OrderPostModel(OrderBaseModel):
    items: Annotated[list[OrderItemsPostModel], Field(min_length=1, max_length=10, alias="items")]

    @field_validator("items", mode="after")
    @classmethod
    def validate_items_unique(cls, value: list[OrderItemsPostModel]) -> list[OrderItemsPostModel]:
        items_id_list = list(map(lambda item: item.book_id, value))
        if len(items_id_list) != len(set(items_id_list)):
            raise ValueError("Items list contains recurring positions!")

        return value

class OrderGetModel(OrderBaseModel):
    id: int
    datetime: datetime
    user_id: Annotated[int, Field(alias="userId")]
    status: OrderStatuses

    user: UserGetModel
    shop: ShopGetModel
    items: Annotated[list[OrderItemsGetModel], Field(alias="items")]
