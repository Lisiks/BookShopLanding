from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String

from .base import Base


class GenresORM(Base):
    __tablename__ = "genres"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), unique=True)