from pydantic import BaseModel, Field, ConfigDict
from typing import Annotated



class AuthorBaseDTO(BaseModel):
    f: Annotated[str, Field(max_length=100)]
    i: Annotated[str, Field(max_length=100)]
    o: Annotated[str, Field(max_length=100)]


    model_config = ConfigDict(from_attributes=True)


class AuthorPostDTO(AuthorBaseDTO):
    ...


class AuthorGetDTO(AuthorBaseDTO):
    id: int