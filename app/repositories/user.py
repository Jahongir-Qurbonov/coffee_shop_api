import datetime
from datetime import UTC

from ..core.database import session
from ..models.user import User


class UserRepository:
    def get(self, pk: str):
        with session() as _session:
            return _session.query(User).filter(User.id == pk).one_or_none()

    def get_by_email(self, email: str):
        with session() as _session:
            return _session.query(User).filter(User.email == email).one_or_none()

    def get_all(self):
        with session() as _session:
            return _session.query(User).all()

    def find_expired_authorizations(self):
        with session() as _session:
            expiration_threshold = datetime.datetime.now(UTC) - datetime.timedelta(
                days=2
            )

            return (
                _session.query(User)
                .filter(
                    (User.created_at < expiration_threshold) & (User.verified == False)  # noqa: E712
                )
                .all()
            )

    def store(self, user: User) -> User:
        with session() as _session:
            _session.add(user)
            _session.commit()
            _session.refresh(user)

            return user

    def delete(self, user: User) -> None:
        with session() as _session:
            _session.delete(user)
            _session.commit()

    def delete_many(self, users: list[User]) -> None:
        with session() as _session:
            for user in users:
                _session.delete(user)
            _session.commit()
