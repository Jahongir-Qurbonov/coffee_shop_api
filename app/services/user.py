from typing import Annotated

from fastapi import Depends


class UserService:
    def __init__(self) -> None:
        pass


UserServiceDep = Annotated[UserService, Depends(UserService)]
