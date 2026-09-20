from pydantic import BaseModel, Field, ConfigDict, field_validator, computed_field
from typing import Annotated, Optional


from ..settings import config


class PaginationBase(BaseModel):
    page: Annotated[int, Field(ge=0, default=0)]


class BookSearchModel(PaginationBase):
    title: Annotated[Optional[str], Field(max_length=200, default=None)]
    min_price: Annotated[Optional[float], Field(gt=0.0, alias="minPrice", default=None)]
    max_price: Annotated[Optional[float], Field(gt=0.0, alias="maxPrice", default=None)]
    jahnre_id: Annotated[Optional[int], Field(gt=0, alias="jahnreId", default=None)]
    author_id: Annotated[Optional[int], Field(gt=0, alias="authorId", default=None)]

    @computed_field
    def limit(self) -> int:
        return config.pagination.books_page_size

    @computed_field
    def offset(self) -> int:
        return self.page * config.pagination.books_page_size


class UsersSearchModel(PaginationBase):
    username: Annotated[Optional[str], Field(max_length=100, default=None)]

    @computed_field
    def limit(self) -> int:
        return config.pagination.users_page_size

    @computed_field
    def offset(self) -> int:
        return self.page * config.pagination.users_page_size


class JahnresSearchModel(BaseModel):
    name: Annotated[Optional[str], Field(max_length=100, default=None)]


class AuthorsSearchModel(BaseModel):
    name_part: Annotated[Optional[str], Field(max_length=100, default=None, alias="namePart")]


class ShopSearchModel(BaseModel):
    address: Annotated[Optional[str], Field(max_length=300, default=None)]