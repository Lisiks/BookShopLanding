from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, ForeignKey, CHAR, Numeric, Text, CheckConstraint
from typing import Optional

from .genres import GenresORM
from .authors import AuthorsORM
from .base import Base


class BooksORM(Base):
    __tablename__ = "books"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(200), index=True)
    description: Mapped[Optional[str]] = mapped_column(Text)
    author_id: Mapped[int] = mapped_column(ForeignKey("authors.id", ondelete="RESTRICT", onupdate="CASCADE", name="authors_id_fk"))
    genre_id: Mapped[int] = mapped_column(ForeignKey("genres.id", ondelete="RESTRICT", onupdate="CASCADE", name="genres_id_fk"))
    page_count: Mapped[int]
    write_year: Mapped[int]
    price: Mapped[float] = mapped_column(Numeric(10, 2), index=True)
    isbn: Mapped[str] = mapped_column(CHAR(17), unique=True)
    image_file_path: Mapped[str] = mapped_column(Text)
    demo_file_path: Mapped[str] = mapped_column(Text)

    author: Mapped["AuthorsORM"] = relationship()
    genre: Mapped["GenresORM"] = relationship()

    __table_args__ = (
        CheckConstraint("page_count > 0", name="page_count_positive_ck"),
        CheckConstraint("price > 0.00", name="price_positive_ck"),
        CheckConstraint("write_year <= EXTRACT(year FROM NOW())", name="write_year_ck"),
    )