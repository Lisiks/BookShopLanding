from pydantic import BaseModel, Field, ConfigDict, field_validator
from typing import Annotated, Optional
from datetime import datetime

from .order_items_dto import OrderItemsGetDTO, OrderItemsPostDTO
from .shops_dto import ShopGetDTO
from .users_dto import UserGetDTO
from ..enums import OrderStatuses


class OrderBaseDTO(BaseModel):
    shop_id: Annotated[int, Field(gt=0, alias="shopId")]

    model_config = ConfigDict(
        from_attributes=True,
        validate_by_alias=True,
        serialize_by_alias=True
    )


class OrderPostDTO(OrderBaseDTO):
    items: Annotated[list[OrderItemsPostDTO], Field(min_length=1, max_length=10, alias="items")]

    @field_validator("items", mode="after")
    @classmethod
    def validate_items_unique(cls, value: list[OrderItemsPostDTO]) -> list[OrderItemsPostDTO]:
        items_id_list = list(map(lambda item: item.book_id, value))
        if len(items_id_list) != len(set(items_id_list)):
            raise ValueError("Items list contains recurring positions!")

        return value

class OrderGetDTO(OrderBaseDTO):
    id: int
    datetime: datetime
    user_id: Annotated[Optional[int], Field(alias="userId", default=None)]
    status: OrderStatuses

    user: Optional[UserGetDTO] = None
    shop: ShopGetDTO
    items: Annotated[list[OrderItemsGetDTO], Field(alias="items")]
