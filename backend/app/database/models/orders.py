from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, DateTime, func, Enum
from typing import Optional
from datetime import datetime

from ...enums import OrderStatuses
from .base import Base
from .shops import ShopsORM
from .users import UsersORM
from .order_items import OrdersItemsORM


class OrdersORM(Base):
    __tablename__ = "orders"

    id: Mapped[int] = mapped_column(primary_key=True)
    datetime: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(), index=True)
    user_id: Mapped[Optional[int]] = mapped_column(ForeignKey("users.id", ondelete="SET NULL", onupdate="CASCADE", name="user_id_fk"))
    status: Mapped[OrderStatuses] = mapped_column(Enum(OrderStatuses), index=True)
    shop_id: Mapped[int] = mapped_column(ForeignKey("shops.id", ondelete="RESTRICT", onupdate="CASCADE", name="shops_id_fk"))

    shop: Mapped["ShopsORM"] = relationship()
    user: Mapped["UsersORM"] = relationship()
    items: Mapped[list["OrdersItemsORM"]] = relationship(cascade="all, delete-orphan")
