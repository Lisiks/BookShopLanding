from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import DateTime, ForeignKey, func, Text, PrimaryKeyConstraint
from typing import Optional
from datetime import datetime

from .base import Base


class CommentsORM(Base):
    __tablename__ = "comments"

    book_id: Mapped[int] = mapped_column(ForeignKey("books.id", name="books_id_fk", ondelete="CASCADE", onupdate="CASCADE"))
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", name="users_id_fk", ondelete="CASCADE", onupdate="CASCADE"))
    
    datetime: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(), index=True)
    text: Mapped[str] = mapped_column(Text)

    __table_args__ = (
        PrimaryKeyConstraint("book_id", "user_id", name="comments_pk"),
    )