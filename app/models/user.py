from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from ..utils import generate_verification_key
from .base import Base


class User(Base):
    __tablename__ = "users"

    email: Mapped[str] = mapped_column(
        String(100),
        unique=True,
        nullable=False,
    )

    first_name: Mapped[str | None] = mapped_column(
        String(50),
        nullable=True,
    )

    last_name: Mapped[str | None] = mapped_column(
        String(50),
        nullable=True,
    )

    is_admin: Mapped[bool] = mapped_column(default=False)

    verification_key: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
        default=generate_verification_key,
    )

    verified: Mapped[bool | None] = mapped_column(default=False)

    hashed_password: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )
