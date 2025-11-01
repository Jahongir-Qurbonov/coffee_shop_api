import contextlib
from datetime import UTC, datetime, timedelta
from typing import Annotated, Any, Literal, TypedDict, cast

import bcrypt
import jwt
from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from ..models.user import User
from ..repositories.user import UserRepository
from .config import settings

ALGORITHM = "HS256"
DEFAULT_TOKEN_EXPIRATION = {
    "access": timedelta(minutes=30),
    "refresh": timedelta(days=7),
}

bearer_auth_scheme = HTTPBearer()


class JwtPayload(TypedDict):
    exp: float
    sub: str
    type: Literal["access", "refresh"]


def create_access_token(
    subject: str | Any,
    expires_delta: timedelta | None = None,
    type: Literal["access", "refresh"] = "access",
) -> str:
    expire = datetime.now(UTC) + (expires_delta or DEFAULT_TOKEN_EXPIRATION[type])

    to_encode = {"exp": expire.timestamp(), "sub": str(subject), "type": type}
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt


def verify_token(token: str):
    with contextlib.suppress(jwt.PyJWTError):
        payload = cast(
            JwtPayload,
            jwt.decode(
                token,
                settings.SECRET_KEY,
                algorithms=[ALGORITHM],
            ),
        )

        print(payload)  # noqa: T201

        if payload["exp"] > datetime.now(UTC).timestamp():
            return payload

    return None


def get_password_hash(password: str) -> str:
    return bcrypt.hashpw(
        password.encode("utf-8"),
        bcrypt.gensalt(),
    ).decode("utf-8")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(
        plain_password.encode("utf-8"),
        hashed_password.encode("utf-8"),
    )


def current_user(
    token: Annotated[HTTPAuthorizationCredentials, Depends(bearer_auth_scheme)],
    user_repository: UserRepository = Depends(use_cache=True),
) -> User | None:
    payload = verify_token(token.credentials)

    if payload:
        user = user_repository.get(payload["sub"])

        if user:
            return user

    raise HTTPException(status_code=401, detail="INVALID_AUTHENTICATION_CREDENTIALS")


def current_verified_user(
    token: Annotated[HTTPAuthorizationCredentials, Depends(bearer_auth_scheme)],
    user_repository: UserRepository = Depends(use_cache=True),
) -> User | None:
    payload = verify_token(token.credentials)

    if payload:
        user = user_repository.get(payload["sub"])

        if user and user.verified:
            return user

    raise HTTPException(status_code=401, detail="INVALID_AUTHENTICATION_CREDENTIALS")


def admin_user(
    token: Annotated[HTTPAuthorizationCredentials, Depends(bearer_auth_scheme)],
    user_repository: UserRepository = Depends(use_cache=True),
) -> User | None:
    payload = verify_token(token.credentials)

    if payload:
        user = user_repository.get(payload["sub"])

        if user and user.is_admin:
            return user

    raise HTTPException(status_code=401, detail="INVALID_AUTHENTICATION_CREDENTIALS")


# Dependency annotations
UserDep = Annotated[User, Depends(current_user)]
VerifiedUserDep = Annotated[User, Depends(current_verified_user)]
AdminUserDep = Annotated[User, Depends(admin_user)]
