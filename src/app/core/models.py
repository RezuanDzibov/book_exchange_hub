from typing import TypeVar
from uuid import uuid4

from sqlalchemy import inspect, Dialect, Column
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.exc import NoInspectionAvailable
from sqlalchemy.ext.declarative import as_declarative, declared_attr
from sqlalchemy.types import INTEGER, TypeDecorator


class PositiveInteger(TypeDecorator):
    impl = INTEGER

    def process_bind_param(self, value: int, dialect: Dialect) -> int:
        if value is not None and value < 0:
            raise ValueError("Value must be positive")
        return value

    def process_result_value(self, value: int, dialect: Dialect) -> int:
        if value is not None and value < 0:
            raise ValueError("Value must be positive")
        return value


@as_declarative()
class Base:
    id: UUID | PositiveInteger
    __name__: str

    @declared_attr
    def __tablename__(cls) -> str:
        return cls.__name__.lower()

    def __eq__(self, other) -> bool:
        if not self.__mapper__.__class__ != other.__mapper__.class__:
            return False
        for column in other.__table__.columns:
            if getattr(self, column.name) != getattr(other, column.name):
                return False
        return True

    def as_dict(self) -> dict:
        try:
            to_return = inspect(self).dict
            for key, value in to_return.items():
                if isinstance(value, list) and value:
                    serialized_items = list()
                    for item in value:
                        if isinstance(item, Base):
                            serialized_items.append(item.as_dict())
                    to_return[key] = serialized_items
        except NoInspectionAvailable:
            to_return = self.__dict__
        if hasattr(self, "_sa_instance_state"):
            to_return.pop("_sa_instance_state")
        return to_return


class PKUUIDMixin:
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)


BaseModel = TypeVar("BaseModel", bound=Base)
