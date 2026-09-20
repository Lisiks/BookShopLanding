from pydantic import BaseModel, Field, ConfigDict, field_validator
from typing import Annotated, Optional
from fastapi import UploadFile
from datetime import datetime, timezone

from .authors_models import AuthorGetModel
from .jahnres_models import JahnreGetModel


IMAGE_FILE_CORRECT_TYPES = {"image/png", "image/jpeg", "image/jpg", "image/bmp", "image/webp"}
DEMO_FILE_CORRECT_TYPES = {"application/pdf"}


class BookBaseModel(BaseModel):

    title: Annotated[str, Field(max_length=200)]
    description: Annotated[Optional[str], Field(default=None)]
    author_id: Annotated[Optional[int], Field(alias="authorId", default=None)]
    jahnre_id: Annotated[Optional[int], Field(gt=0, alias="jahnreId", default=None)]
    page_count: Annotated[int, Field(gt=0, alias="pageCount")]
    write_year: Annotated[int, Field(alias="writeYear")]
    price: Annotated[float, Field(gt=0.0, lt=100000000)]
    isbn: Annotated[str, Field(min_length=17, max_length=17)]

    model_config = ConfigDict(
        from_attributes=True,
        validate_by_alias=True,
        serialize_by_alias=True,
        extra="ignore"
    )


class BookPostModel(BookBaseModel):

    image_file: Annotated[UploadFile, Field(alias="imageFile", exclude=True)]
    demo_file: Annotated[UploadFile, Field(alias="demoFile", exclude=True)]
    

    @field_validator("write_year", mode="after")
    @classmethod
    def validate_year(cls, value: int) -> int:
        if value > datetime.now(timezone.utc).year:
            raise ValueError("Year cannot be greather than today year.")
        return value


    @field_validator("image_file", mode="after")
    @classmethod
    def validate_image_file(cls, value: UploadFile) -> UploadFile:
        if value.content_type not in IMAGE_FILE_CORRECT_TYPES:
            raise ValueError(f"Image content type is incorrect. Correct types: {IMAGE_FILE_CORRECT_TYPES}")
        return value

    @field_validator("demo_file", mode="after")
    @classmethod
    def validate_demo_file(cls, value: Optional[UploadFile]) -> Optional[UploadFile]:
        if value.content_type not in DEMO_FILE_CORRECT_TYPES:
            raise ValueError(f"Demo file content type is incorrect. Correct types: {DEMO_FILE_CORRECT_TYPES}")
        return value


class BookGetModelWithoutORM(BookBaseModel):
    id: int
    image_file_path: Annotated[str, Field(alias="imageFilePath")]
    demo_file_path: Annotated[str, Field(alias="demoFilePath", default=None)]


class BookGetModel(BookGetModelWithoutORM):
    author: Optional[AuthorGetModel]
    jahnre: Optional[JahnreGetModel]

