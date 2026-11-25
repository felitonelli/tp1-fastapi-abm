from pydantic import BaseModel
from typing import List, Optional


class User(BaseModel):
    id: int
    name: str
    is_active: bool = True  # default value, field becomes optional


# PUT: reemplaza todos los datos del usuario (el id viene en la URL)
class UpdateUserRequest(BaseModel):
    name: str
    is_active: bool


# PATCH: modifica solo los campos que se manden
class PatchUserRequest(BaseModel):
    name: Optional[str] = None
    is_active: Optional[bool] = None


class GetUsersResponse(BaseModel):
    users: List[User]


class CreateUserResponse(BaseModel):
    message: str


class DeleteUserResponse(BaseModel):
    message: str
