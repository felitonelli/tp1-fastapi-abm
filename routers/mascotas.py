from typing import Optional

from fastapi import APIRouter, HTTPException, status
from models.mascotas import (
    Mascota,
    MascotaRequest,
    PatchMascotaRequest,
    GetMascotasResponse,
    DeleteMascotaResponse,
)

router = APIRouter(tags=["Mascotas"])

# Almacenamiento en memoria
mascotas: list[Mascota] = [
    Mascota(id=1, nombre="Toby", especie="perro", raza="caniche", edad=5),
    Mascota(id=2, nombre="Michi", especie="gato", raza="siames", edad=2),
    Mascota(id=3, nombre="Rocco", especie="perro", raza="labrador", edad=9),
]


def siguiente_id() -> int:
    return max((m.id for m in mascotas), default=0) + 1


def buscar_mascota(id: int) -> Mascota:
    for mascota in mascotas:
        if mascota.id == id:
            return mascota
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Mascota no encontrada"
    )


@router.post("/mascotas", status_code=status.HTTP_201_CREATED)
def create_mascota(datos: MascotaRequest) -> Mascota:
    mascota = Mascota(id=siguiente_id(), **datos.model_dump())
    mascotas.append(mascota)
    return mascota


@router.get("/mascotas")
def get_mascotas(
    especie: Optional[str] = None,
    nombre: Optional[str] = None,
    edad_max: Optional[int] = None,
) -> GetMascotasResponse:
    """Lista mascotas. Filtros opcionales (se pueden combinar):
    - especie: exacta, sin distinguir mayúsculas (ej: perro)
    - nombre: parte del nombre (ej: to)
    - edad_max: mascotas con esa edad o menos
    """
    resultado = mascotas
    if especie is not None:
        resultado = [m for m in resultado if m.especie.lower() == especie.lower()]
    if nombre is not None:
        resultado = [m for m in resultado if nombre.lower() in m.nombre.lower()]
    if edad_max is not None:
        resultado = [m for m in resultado if m.edad <= edad_max]
    return GetMascotasResponse(mascotas=resultado)


@router.get("/mascotas/{id}")
def get_mascota(id: int) -> Mascota:
    return buscar_mascota(id)


@router.put("/mascotas/{id}")
def update_mascota(id: int, datos: MascotaRequest) -> Mascota:
    mascota = buscar_mascota(id)
    mascota.nombre = datos.nombre
    mascota.especie = datos.especie
    mascota.raza = datos.raza
    mascota.edad = datos.edad
    return mascota


@router.patch("/mascotas/{id}")
def patch_mascota(id: int, datos: PatchMascotaRequest) -> Mascota:
    mascota = buscar_mascota(id)
    # exclude_unset: solo los campos que vinieron en el body
    for campo, valor in datos.model_dump(exclude_unset=True).items():
        if valor is not None:
            setattr(mascota, campo, valor)
    return mascota


@router.delete("/mascotas/{id}")
def delete_mascota(id: int) -> DeleteMascotaResponse:
    mascota = buscar_mascota(id)
    mascotas.remove(mascota)
    return DeleteMascotaResponse(message="mascota borrada")
