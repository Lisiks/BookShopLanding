from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, Numeric, PrimaryKeyConstraint, CheckConstraint

from .base import Base
from .books import BooksORM

class OrdersItemsORM(Base):
    __tablename__ = "orders_items"

    order_id: Mapped[int] = mapped_column(ForeignKey("orders.id", name="orders_id_fk", ondelete="CASCADE", onupdate="CASCADE"))
    book_id: Mapped[int] = mapped_column(ForeignKey("books.id", name="books_id_fk", ondelete="SET NULL", onupdate="CASCADE"))

    count: Mapped[int]
    price: Mapped[float] = mapped_column(Numeric(10, 2))

    book: Mapped["BooksORM"] = relationship()


    __table_args__ = (
        CheckConstraint("count > 0", name="count_positive_ck"),
        PrimaryKeyConstraint("order_id", "book_id", name="orders_items_pk")
    )