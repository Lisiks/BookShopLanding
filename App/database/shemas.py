from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy import String, Text, ForeignKey, Numeric, CHAR, CheckConstraint, Table, Column, PrimaryKeyConstraint, Boolean, DateTime, func, Enum, Index, UniqueConstraint
from typing import Optional
from datetime import datetime
import enum



class Base(DeclarativeBase):
    ...


class Jahnres(Base):
    __tablename__ = "jahnres"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), unique=True)


class Authors(Base):
    __tablename__ = "authors"

    id: Mapped[int] = mapped_column(primary_key=True)
    f: Mapped[str] = mapped_column(String(100))
    i: Mapped[str] = mapped_column(String(100))
    o: Mapped[str] = mapped_column(String(100))




class Books(Base):
    __tablename__ = "books"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(200), index=True)
    description: Mapped[Optional[str]] = mapped_column(Text)
    author_id: Mapped[Optional[int]] = mapped_column(ForeignKey("authors.id", ondelete="SET NULL", onupdate="CASCADE", name="authors_id_fk"))
    jahnre_id: Mapped[Optional[int]] = mapped_column(ForeignKey("jahnres.id", ondelete="SET NULL", onupdate="CASCADE", name="jahnres_id_fk"))
    page_count: Mapped[int]
    write_year: Mapped[int]
    price: Mapped[float] = mapped_column(Numeric(10, 2), index=True)
    isbn: Mapped[str] = mapped_column(CHAR(17), unique=True)
    image_file_path: Mapped[str] = mapped_column(Text)
    demo_file_path: Mapped[Optional[str]] = mapped_column(Text)

    author: Mapped["Authors"] = relationship()
    jahnre: Mapped["Jahnres"] = relationship()

    __table_args__ = (
        CheckConstraint("page_count > 0", name="page_count_positive_ck"),
        CheckConstraint("price > 0.00", name="price_positive_ck"),
        CheckConstraint("write_year <= EXTRACT(year FROM NOW())", name="write_year_ck"),
    )


class Users(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(100), unique=True)
    password_hash: Mapped[str] = mapped_column(Text)
    is_admin: Mapped[bool] = mapped_column(Boolean, default=False, server_default="FALSE", index=True)
    is_blocked: Mapped[bool] = mapped_column(Boolean, default=False, server_default="FALSE")



class OrderStatuses(enum.Enum):
    InAssembly = "В сборке"
    Assembled = "Собран"
    Received = "Получен"
    Canceled = "Отменен"



class Shops(Base):
    __tablename__ = "shops"

    id: Mapped[int] = mapped_column(primary_key=True)
    phone: Mapped[str] = mapped_column(String(20), unique=True)

    town: Mapped[str] = mapped_column(String(100))
    street: Mapped[str] = mapped_column(String(100))
    housing: Mapped[str] = mapped_column(String(6))

    __table_args__ = (
        UniqueConstraint("town", "street", "housing", name="address_uq"),
    )



class Orders(Base):
    __tablename__ = "orders"

    id: Mapped[int] = mapped_column(primary_key=True)
    datetime: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    user_id: Mapped[Optional[int]] = mapped_column(ForeignKey("users.id", ondelete="SET NULL", onupdate="CASCADE", name="user_id_fk"))
    status: Mapped[OrderStatuses] = mapped_column(Enum(OrderStatuses), index=True)
    shop_id: Mapped[Optional[int]] = mapped_column(ForeignKey("shops.id", ondelete="SET NULL", onupdate="CASCADE", name="shops_id_fk"))

    shop: Mapped["Shops"] = relationship()
    user: Mapped["Users"] = relationship()
    items: Mapped[list["OrdersItems"]] = relationship(cascade="all, delete-orphan")


class OrdersItems(Base):
    __tablename__ = "orders_items"

    order_id: Mapped[int] = mapped_column(ForeignKey("orders.id", name="orders_id_fk", ondelete="CASCADE", onupdate="CASCADE"))
    book_id: Mapped[int] = mapped_column(ForeignKey("books.id", name="books_id_fk", ondelete="SET NULL", onupdate="CASCADE"))

    count: Mapped[int]
    price: Mapped[float] = mapped_column(Numeric(10, 2))

    book: Mapped["Books"] = relationship()


    __table_args__ = (
        CheckConstraint("count > 0", name="count_positive_ck"),
        PrimaryKeyConstraint("order_id", "book_id", name="orders_items_pk")
    )


class Comments(Base):
    __tablename__ = "comments"

    book_id: Mapped[int] = mapped_column(ForeignKey("books.id", name="books_id_fk", ondelete="CASCADE", onupdate="CASCADE"))
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", name="users_id_fk", ondelete="CASCADE", onupdate="CASCADE"))
    
    datetime: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    text: Mapped[str] = mapped_column(Text)

    user: Mapped["Users"] = relationship()

    __table_args__ = (
        PrimaryKeyConstraint("book_id", "user_id", name="comments_pk"),
    )

