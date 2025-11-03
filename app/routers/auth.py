from fastapi import APIRouter, Depends, HTTPException
from fastapi import status as http_status

from ..core.security import (
    UserDep,
    create_access_token,
    get_password_hash,
    verify_password,
    verify_token,
)
from ..models.user import User
from ..repositories.user import UserRepository
from ..schemas.auth import (
    LoginRequest,
    LoginResponse,
    RefreshRequest,
    RefreshResponse,
    SignUpRequest,
    VerifyRequest,
)

router = APIRouter(tags=["login"])


@router.post(
    "/signup",
    responses={
        http_status.HTTP_400_BAD_REQUEST: {
            "content": {
                "application/json": {"example": {"detail": "USER_ALREADY_EXISTS"}}
            }
        },
    },
)
async def signup(
    data: SignUpRequest,
    user_repository: UserRepository = Depends(),
) -> None:
    user = user_repository.get_by_email(data.email)

    if user:
        raise HTTPException(
            status_code=http_status.HTTP_400_BAD_REQUEST,
            detail="USER_ALREADY_EXISTS",
        )

    new_user = User(
        email=data.email,
        first_name=data.first_name,
        last_name=data.last_name,
        hashed_password=get_password_hash(data.password),
    )

    user_repository.store(new_user)

    print(  # noqa: T201
        f"New user signed up: {new_user.email}, verification key: {new_user.verification_key}"
    )


@router.post(
    "/login",
    responses={
        http_status.HTTP_401_UNAUTHORIZED: {
            "content": {
                "application/json": {"example": {"detail": "INVALID_EMAIL_OR_PASSWORD"}}
            }
        },
    },
)
async def login(
    data: LoginRequest,
    user_repository: UserRepository = Depends(),
) -> LoginResponse:
    user = user_repository.get_by_email(data.email)

    if user:
        if verify_password(data.password, user.hashed_password):
            access_token = create_access_token(subject=user.id)
            refresh_token = create_access_token(subject=user.id, type="refresh")

            return LoginResponse(access_token=access_token, refresh_token=refresh_token)

    raise HTTPException(
        status_code=http_status.HTTP_401_UNAUTHORIZED,
        detail="INVALID_EMAIL_OR_PASSWORD",
    )


@router.post(
    "/refresh",
    responses={
        http_status.HTTP_401_UNAUTHORIZED: {
            "content": {
                "application/json": {"example": {"detail": "INVALID_REFRESH_TOKEN"}}
            }
        },
    },
)
async def refresh(
    data: RefreshRequest,
    user: UserDep,  # noqa: ARG001
) -> RefreshResponse:
    payload = verify_token(data.refresh_token)

    if payload:
        new_access_token = create_access_token(subject=payload["sub"])

        return RefreshResponse(
            access_token=new_access_token,
            refresh_token=data.refresh_token,
        )

    raise HTTPException(
        status_code=http_status.HTTP_401_UNAUTHORIZED,
        detail="INVALID_REFRESH_TOKEN",
    )


@router.post(
    "/verify",
    responses={
        http_status.HTTP_400_BAD_REQUEST: {
            "content": {
                "application/json": {"example": {"detail": "INVALID_VERIFICATION_KEY"}}
            }
        },
    },
)
async def verify(
    data: VerifyRequest,
    user: UserDep,
    user_repository: UserRepository = Depends(),
) -> None:
    if user.verification_key == data.key:
        user.verified = True
        user.verification_key = None
        user_repository.store(user)

        return

    raise HTTPException(
        status_code=http_status.HTTP_400_BAD_REQUEST,
        detail="INVALID_VERIFICATION_KEY",
    )
