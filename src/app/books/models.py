from datetime import datetime
from typing import List

from sqlalchemy import String, ForeignKey, Enum, Table, Column, Boolean, DateTime, DATETIME
from sqlalchemy.orm import relationship, Mapped, mapped_column
from sqlalchemy.dialects.postgresql import UUID

from core.models import Base, PKUUIDMixin, PositiveInteger
from users.models import User
from books.enums import ConditionEnum, BookExchangeStatus


user_book_mtm_book_request_association_table = Table(
    "user_book_mtm_book_request_association_table",
    Base.metadata,
    Column("user_book_id", ForeignKey("userbook.id"), primary_key=True),
    Column("book_request_id", ForeignKey("bookrequest.id"), primary_key=True),
)


class Category(PKUUIDMixin, Base):
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
    user_id: Mapped[UUID] = mapped_column(ForeignKey("user.id"))
    user: Mapped["User"] = relationship(back_populates="books")
    book_id: Mapped[UUID] = mapped_column(ForeignKey("book.id"))
    condition: Mapped[Enum] = mapped_column(Enum(ConditionEnum))
    in_book_requests: Mapped[List["BookRequest"]] = relationship(
        secondary=user_book_mtm_book_request_association_table,
        back_populates="user_books"
    )


class BookRequest(PKUUIDMixin, Base):
    user_id: Mapped[UUID] = mapped_column(ForeignKey("user.id"))
    user: Mapped["User"] = relationship(back_populates="bookrequests")
    book_id: Mapped[UUID] = mapped_column(ForeignKey("book.id"))
    exchangeable_books: Mapped[List["UserBook"]] = relationship(
        secondary=user_book_mtm_book_request_association_table,
        back_populates="in_book_requests"
    )
    is_active: Mapped[bool] = mapped_column(Boolean)


class BookExchange(PKUUIDMixin, Base):
    book_request_id: Mapped[UUID] = mapped_column(ForeignKey("bookrequest.id"))
    book_request: Mapped["BookRequest"] = relationship(backref="book_exchange")
    status: Mapped[Enum] = mapped_column(Enum(BookExchangeStatus))
    created_at: Mapped[DATETIME] = mapped_column(DateTime, default=datetime.now)
    exchanged_at: Mapped[DATETIME] = mapped_column(DateTime, default=datetime.now)
    requested_book: Mapped[UUID] = mapped_column(ForeignKey("book.id"))
    book_in_exchange: Mapped[UUID] = mapped_column(ForeignKey("userbook.id"))
