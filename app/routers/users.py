from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Path
from fastapi import status as http_status

from ..core.security import AdminUserDep, UserDep
from ..repositories.user import UserRepository
from ..schemas.user import UserListResponse, UserResponse, UserUpdateRequest

router = APIRouter(tags=["users"])


@router.get("/me")
async def me(user: UserDep) -> UserResponse:
    return UserResponse.model_validate(user)


@router.get("/users")
async def users(
    user: AdminUserDep,  # noqa: ARG001
    user_repository: UserRepository = Depends(),
) -> UserListResponse:
    users = user_repository.get_all()

    return [UserResponse.model_validate(u) for u in users]


@router.get(
    "/users/{id}",
    responses={
        http_status.HTTP_404_NOT_FOUND: {
            "content": {"application/json": {"example": {"detail": "USER_NOT_FOUND"}}}
        },
    },
)
async def get_user(
    user: AdminUserDep,  # noqa: ARG001
    user_id: Annotated[str, Path(alias="id")],
    user_repository: UserRepository = Depends(),
) -> UserResponse:
    target_user = user_repository.get(user_id)

    if not target_user:
        raise HTTPException(
            status_code=http_status.HTTP_404_NOT_FOUND, detail="USER_NOT_FOUND"
        )

    return UserResponse.model_validate(target_user)


@router.patch(
    "/users/{id}",
    responses={
        http_status.HTTP_403_FORBIDDEN: {
            "content": {
                "application/json": {
                    "example": {"detail": "NOT_AUTHORIZED_TO_UPDATE_THIS_USER"}
                }
            }
        },
        http_status.HTTP_404_NOT_FOUND: {
            "content": {"application/json": {"example": {"detail": "USER_NOT_FOUND"}}}
        },
    },
)
async def update_user(
    data: UserUpdateRequest,
    user: UserDep,
    user_id: Annotated[str, Path(alias="id")],
    user_repository: UserRepository = Depends(),
) -> UserResponse:
    if not user.is_admin and user.id != user_id:
        raise HTTPException(
            status_code=http_status.HTTP_403_FORBIDDEN,
            detail="NOT_AUTHORIZED_TO_UPDATE_THIS_USER",
        )

    target_user = user_repository.get(user_id)

    if not target_user:
        raise HTTPException(
            status_code=http_status.HTTP_404_NOT_FOUND,
            detail="USER_NOT_FOUND",
        )

    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(target_user, field, value)

    user_repository.store(target_user)

    return UserResponse.model_validate(target_user)


@router.delete(
    "/users/{id}",
    responses={
        http_status.HTTP_404_NOT_FOUND: {
            "content": {"application/json": {"example": {"detail": "USER_NOT_FOUND"}}}
        },
        http_status.HTTP_400_BAD_REQUEST: {
            "content": {
                "application/json": {
                    "example": {"detail": "ADMIN_USERS_CANNOT_DELETE_THEMSELVES"}
                }
            }
        },
        http_status.HTTP_403_FORBIDDEN: {
            "content": {
                "application/json": {
                    "example": {"detail": "CANNOT_DELETE_ANOTHER_ADMIN_USER"}
                }
            }
        },
    },
)
async def delete_user(
    user: AdminUserDep,
    user_id: Annotated[str, Path(alias="id")],
    user_repository: UserRepository = Depends(),
) -> None:
    target_user = user_repository.get(user_id)

    if not target_user:
        raise HTTPException(
            status_code=http_status.HTTP_404_NOT_FOUND,
            detail="USER_NOT_FOUND",
        )

    if target_user.id == user.id:
        raise HTTPException(
            status_code=http_status.HTTP_400_BAD_REQUEST,
            detail="ADMIN_USERS_CANNOT_DELETE_THEMSELVES",
        )

    if target_user.is_admin:
        raise HTTPException(
            status_code=http_status.HTTP_403_FORBIDDEN,
            detail="CANNOT_DELETE_ANOTHER_ADMIN_USER",
        )

    user_repository.delete(target_user)
