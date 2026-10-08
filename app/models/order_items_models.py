from pydantic import BaseModel, Field, ConfigDict, field_validator
from typing import Annotated

from ..models.books_models import BookShortModel


class OrderItemsBaseModel(BaseModel):
    book_id: Annotated[int, Field(gt=0, alias="bookId")]
    count: Annotated[int, Field(gt=0, le=20)]

    model_config = ConfigDict(
        from_attributes=True,
        validate_by_alias=True,
        serialize_by_alias=True
    )


class OrderItemsPostModel(OrderItemsBaseModel):
    ...


class OrderItemsGetModel(OrderItemsBaseModel):
    price: float
    order_id: Annotated[int, Field(gt=0, alias="orderId")]
    book: BookShortModel


  



