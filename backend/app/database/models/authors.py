from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Index

from .base import Base


class AuthorsORM(Base):
    __tablename__ = "authors"

    id: Mapped[int] = mapped_column(primary_key=True)
    f: Mapped[str] = mapped_column(String(100))
    i: Mapped[str] = mapped_column(String(100))
    o: Mapped[str] = mapped_column(String(100))

    __table_args__ = (
        Index("fio_idx", "f", "i", "o", unique=False),
    )
