from collections.abc import Generator
from contextlib import contextmanager

from sqlalchemy.engine import create_engine
from sqlalchemy.orm import Session, scoped_session, sessionmaker

from .config import settings

# Cache scoped session
__session_factory: scoped_session | None = None


def get_session_factory() -> scoped_session[Session]:
    global __session_factory

    if __session_factory is None:
        engine = create_engine(
            str(settings.SQLALCHEMY_DATABASE_URI),
            echo=False,
        )

        __session_factory = scoped_session(
            sessionmaker(
                bind=engine,
                autocommit=False,
                autoflush=False,
            )
        )

    return __session_factory


@contextmanager
def session() -> Generator[Session]:
    _session_factory = get_session_factory()
    _session = _session_factory()

    try:
        yield _session
    except Exception:
        _session.rollback()
        raise
    finally:
        _session.close()
