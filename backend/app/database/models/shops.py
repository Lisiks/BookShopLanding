from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Index

from .base import Base


class ShopsORM(Base):
    __tablename__ = "shops"

    id: Mapped[int] = mapped_column(primary_key=True)
    phone: Mapped[str] = mapped_column(String(20), unique=True)

    town: Mapped[str] = mapped_column(String(100))
    street: Mapped[str] = mapped_column(String(100))
    housing: Mapped[str] = mapped_column(String(6))

    __table_args__ = (
        Index("address_idx", "town", "street", "housing", unique=True),
    )