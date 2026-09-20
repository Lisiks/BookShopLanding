from pydantic import BaseModel, Field, ConfigDict
from typing import Annotated


class JahnreBaseModel(BaseModel):
    name: Annotated[str, Field(max_length=100)]

    model_config = ConfigDict(from_attributes=True)


class JahnrePostModel(JahnreBaseModel):
    ...


class JahnreGetModel(JahnreBaseModel):
    id: int