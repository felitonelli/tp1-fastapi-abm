from typing import Optional

from fastapi import APIRouter, HTTPException, status
from models.users import (
    User,
    UpdateUserRequest,
    PatchUserRequest,
    GetUsersResponse,
    CreateUserResponse,
    DeleteUserResponse,
)

router = APIRouter(tags=["Usuarios"])

usuarios: list[User] = [
    User(id=1, name="juan perez"),
    User(id=2, name="pepe sanchez"),
    User(id=3, name="ana gomez", is_active=False),
]


def buscar_usuario(id: int) -> User:
    for user in usuarios:
        if user.id == id:
            return user
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Usuario no encontrado"
    )


@router.get("/user")
def get_users(is_active: Optional[bool] = None) -> GetUsersResponse:
    """Lista usuarios. Filtro opcional por estado:
    - sin is_active: todos
    - is_active=true: solo activos
    - is_active=false: solo inactivos
    """
    if is_active is None:
        return GetUsersResponse(users=usuarios)
    filtrados = [u for u in usuarios if u.is_active == is_active]
    return GetUsersResponse(users=filtrados)


@router.get("/user/{id}")
def get_user(id: int) -> User:
    return buscar_usuario(id)


@router.post("/user", status_code=status.HTTP_201_CREATED)
def create_user(user: User) -> CreateUserResponse:
    if any(u.id == user.id for u in usuarios):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Ya existe un usuario con ese id"
        )
    usuarios.append(user)
    return CreateUserResponse(message="usuario creado")


@router.put("/user/{id}")
def update_user(id: int, datos: UpdateUserRequest) -> User:
    user = buscar_usuario(id)
    user.name = datos.name
    user.is_active = datos.is_active
    return user


@router.patch("/user/{id}")
def patch_user(id: int, datos: PatchUserRequest) -> User:
    user = buscar_usuario(id)
    if datos.name is not None:
        user.name = datos.name
    if datos.is_active is not None:
        user.is_active = datos.is_active
    return user


@router.delete("/user/{id}")
def delete_user(id: int) -> DeleteUserResponse:
    user = buscar_usuario(id)
    usuarios.remove(user)
    return DeleteUserResponse(message="usuario borrado")
