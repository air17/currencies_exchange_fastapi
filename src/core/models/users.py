from sqlalchemy.orm import relationship

from .base import Base, TimestampMixin
from fastapi_users.db import SQLAlchemyBaseUserTableUUID


class User(SQLAlchemyBaseUserTableUUID, TimestampMixin, Base):
    """Base User model with UUID as primary key and timestamp columns."""
