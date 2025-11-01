from pydantic import BaseModel, ConfigDict, EmailStr


class UserResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    email: EmailStr
    first_name: str
    last_name: str
    verified: bool


UserListResponse = list[UserResponse]


class UserUpdateRequest(BaseModel):
    first_name: str | None
    last_name: str | None
