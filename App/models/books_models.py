from pydantic import BaseModel, Field, ConfigDict, field_validator
from typing import Annotated, Optional
from fastapi import UploadFile
from datetime import datetime, timezone

from .authors_models import AuthorGetModel
from .jahnres_models import JahnreGetModel


__IMAGE_FILE_CORRECT_TYPES = {"image/png", "image/jpeg", "image/jpg", "image/bmp", "image/webp"}
__DEMO_FILE_CORRECT_TYPES = {"application/pdf"}


class BookBaseModel(BaseModel):

    title: Annotated[str, Field(max_length=200)]
    description: Annotated[Optional[str], Field(default=None)]
    author_id: Annotated[int, Field(alias="authorId")]
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

    image_file: Annotated[UploadFile, Field(alias="imageFile")]
    demo_file: Annotated[UploadFile, Field(alias="demoFile")]
    jahnres: list[int]

    @field_validator("write_year", mode="after")
    @classmethod
    def validate_year(cls, value: int) -> int:
        if value > datetime.now(timezone.utc):
            raise ValueError("Year cannot be greather than today year.")
        return value


    @field_validator("image_file", mode="after")
    @classmethod
    def validate_year(cls, value: UploadFile) -> UploadFile:
        if value.content_type not in __IMAGE_FILE_CORRECT_TYPES:
            raise ValueError("Image content type is incorrect. Correct types: {__IMAGE_FILE_CORRECT_TYPES}")
        return value

    @field_validator("demo_file", mode="after")
    @classmethod
    def validate_year(cls, value: Optional[UploadFile]) -> Optional[UploadFile]:
        if value is not None and value.content_type not in __DEMO_FILE_CORRECT_TYPES:
            raise ValueError(f"Demo file content type is incorrect. Correct types: {__DEMO_FILE_CORRECT_TYPES} ")
        return value


class BookGetModel(BookBaseModel):
    id: int
    image_file_path: Annotated[str, Field(alias="imageFilePath")]
    demo_file_path: Annotated[str, Field(alias="demoFilePath")]
    author: AuthorGetModel
    jahnres: list[JahnreGetModel]




class BookSinpleModel(BaseModel):
    id: int
    title: Annotated[str, Field(max_length=200)]

    model_config = ConfigDict(
        from_attributes=True,
        extra="ignore"
    )