from pydantic import BaseModel, Field, ConfigDict
from typing import Annotated
from datetime import datetime

class CommentGetModel(BaseModel):
    text: Annotated[str, Field(min_length=3, max_length=1000)]
    datetime: datetime
    user_id: int
    username: str

    model_config = ConfigDict(
        from_attributes=True
    )
