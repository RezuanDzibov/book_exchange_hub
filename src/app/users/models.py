from datetime import datetime

from sqlalchemy import Column, String, Boolean, DATETIME


class BaseUser:
    username = Column(String(length=255), unique=True)
    email = Column(String(length=255), unique=True)
    password = Column(String(length=255))
    is_active = Column(Boolean, default=False)
    is_superuser = Column(Boolean, default=False)
    join_date_time = Column(DATETIME, default=datetime.now)
