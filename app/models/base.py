from datetime import datetime

from sqlalchemy import func, types
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from ulid import ULID


class Base(DeclarativeBase):
    __abstract__ = True

    id: Mapped[str] = mapped_column(
        types.String(26),
        default=lambda: str(ULID()),
        primary_key=True,
    )

    created_at: Mapped[datetime] = mapped_column(
        types.DateTime(timezone=True),
        server_default=func.now(),
    )

    updated_at: Mapped[datetime] = mapped_column(
        types.DateTime(timezone=True),
        server_default=func.now(),
        server_onupdate=func.now(),
    )
