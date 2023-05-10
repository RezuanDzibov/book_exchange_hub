from datetime import datetime

from sqlalchemy import Column, String, Boolean, DATETIME

from src.app.core.models import PKUUIDMixin, Base


class BaseUser:
    username = Column(String(length=255), unique=True)
    email = Column(String(length=255), unique=True)
    password = Column(String(length=255))
    is_active = Column(Boolean, default=False)
    is_superuser = Column(Boolean, default=False)
    join_date_time = Column(DATETIME, default=datetime.now)


class User(PKUUIDMixin, Base):
    first_name = Column(String(length=255))
    last_name = Column(String(length=255))
    birth_date = Column(String, nullable=True)
