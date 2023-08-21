from datetime import datetime

from sqlalchemy import func
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    """Base class for all models."""

    # Generate __tablename__ automatically
    @declared_attr.directive
    def __tablename__(cls) -> str:
        """Returns the lowercase name of the class as the table name."""
        return cls.__name__.lower()

    id: Mapped[int] = mapped_column(primary_key=True)


class TimestampMixin:
    """Mixin for adding timestamp columns."""
    created_at: Mapped[datetime] = mapped_column(default=func.now())
    updated_at: Mapped[datetime] = mapped_column(default=func.now(), onupdate=func.now())
