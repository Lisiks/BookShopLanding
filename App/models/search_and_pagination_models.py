from pydantic import BaseModel, Field, ConfigDict, field_validator, computed_field
from typing import Annotated, Optional


from ..settings import config


class PaginationBase(BaseModel):
    page: Annotated[int, Field(ge=0)]


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