from pydantic import BaseModel, Field, ConfigDict
from typing import Annotated


class AuthorBaseMode(BaseModel):
    f: Annotated[str, Field(max_length=100)]
    i: Annotated[str, Field(max_length=100)]
    o: Annotated[str, Field(max_length=100)]


    model_config = ConfigDict(from_attributes=True)


class AuthorPostModel(AuthorBaseMode):
    ...


class AuthorGetModel(AuthorBaseMode):
    id: int