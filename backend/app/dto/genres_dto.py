from pydantic import BaseModel, Field, ConfigDict
from typing import Annotated


class GenreBaseDTO(BaseModel):
    name: Annotated[str, Field(max_length=100)]

    model_config = ConfigDict(from_attributes=True)


class GenrePostDTO(GenreBaseDTO):
    ...


class GenreGetDTO(GenreBaseDTO):
    id: int