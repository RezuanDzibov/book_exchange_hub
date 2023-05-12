from datetime import datetime
from typing import List

from sqlalchemy import String, ForeignKey, Enum, Table, Column, Boolean, DATETIME
from sqlalchemy.orm import relationship, Mapped, mapped_column
from sqlalchemy.dialects.postgresql import UUID

from src.app.core.models import Base, PKUUIDMixin, PositiveInteger
from src.app.users.models import User
from src.app.books.enums import ConditionEnum, BookExchangeStatus


user_book_mtm_book_request_association_table = Table(
    "user_book_mtm_book_request_association_table",
    Base.metadata,
    Column("user_book_id", ForeignKey("user_book.id"), primary_key=True),
    Column("book_request_id", ForeignKey("book_request.id"), primary_key=True),
)


class Category(PKUUIDMixin):
    title: Mapped[str] = mapped_column(String(length=255))
    books: Mapped[List["Book"]] = relationship(back_populates="category")


class Book(PKUUIDMixin, Base):
    title: Mapped[str] = mapped_column(String(255))
    author: Mapped[str] = mapped_column(String(255))
    isbn: Mapped[str] = mapped_column(String(length=13))
    pages: Mapped[int] = mapped_column(PositiveInteger())
    category_id: Mapped[UUID] = mapped_column(ForeignKey("category.id"))
    category: Mapped["Category"] = relationship(back_populates="books")


class UserBook(PKUUIDMixin, Base):
    user_id: Mapped[PKUUIDMixin] = mapped_column(ForeignKey("user.id"))
    user: Mapped["User"] = relationship(back_populates="books")
    book_id: Mapped[UUID] = mapped_column(ForeignKey("book.id"))
    condition: Mapped[Enum] = mapped_column(Enum(ConditionEnum))
    in_book_requests: Mapped[List["BookRequest"]] = relationship(
        secondary=user_book_mtm_book_request_association_table,
        back_populates="user_books"
    )


class BookRequest(PKUUIDMixin, Base):
    user_id: Mapped[PKUUIDMixin] = mapped_column(ForeignKey("user.id"))
    user: Mapped["User"] = relationship(back_populates="book_requests")
    book_id: Mapped[PKUUIDMixin] = mapped_column(ForeignKey("book.id"))
    exchangeable_books: Mapped[List["Book"]] = relationship(
        secondary=user_book_mtm_book_request_association_table,
        back_populates="in_book_requests"
    )
    active: Mapped[bool] = mapped_column(Boolean)


class BookExchange(PKUUIDMixin, Base):
    book_request_id: Mapped[UUID] = mapped_column(ForeignKey("book_request.id"))
    book_request: Mapped["BookRequest"] = relationship(backref="book_exchange")
    status: Mapped[Enum] = mapped_column(Enum(BookExchangeStatus))
    created_at: Mapped[DATETIME] = mapped_column(DATETIME, default=datetime.now)
    exchanged_at: Mapped[DATETIME] = mapped_column(DATETIME, default=datetime.now)
    requested_book: Mapped[PKUUIDMixin] = mapped_column(ForeignKey("user_book.id"))
    book_in_exchange: Mapped[PKUUIDMixin] = mapped_column(ForeignKey("user_book.id"))
