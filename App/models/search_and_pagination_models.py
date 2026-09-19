from pydantic import BaseModel, Field, ConfigDict, field_validator, computed_field
from typing import Annotated, Optional


from ..core.settings import config


class PaginationBase(BaseModel):
    page: Annotated[int, Field(ge=0)]


class UsersSearchAndPaginationModel(PaginationBase):
    @computed_field("limit")
    def limit(self) -> int:
        return config.pagination.users_page_size

    @computed_field("offset")
    def offset(self) -> int:
        return self.page * config.pagination.users_page_size