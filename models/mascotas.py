from pydantic import BaseModel, Field
from typing import List, Optional


# Entidad propia: Mascota (5 campos: id, nombre, especie, raza, edad)
class Mascota(BaseModel):
    id: int
    nombre: str
    especie: str
    raza: str
    edad: int = Field(ge=0)  # en años, no puede ser negativa


# Alta y PUT: todos los campos menos el id (lo asigna la API / viene en la URL)
class MascotaRequest(BaseModel):
    nombre: str
    especie: str
    raza: str
    edad: int = Field(ge=0)


# PATCH: solo los campos que se quieran cambiar
class PatchMascotaRequest(BaseModel):
    nombre: Optional[str] = None
    especie: Optional[str] = None
    raza: Optional[str] = None
    edad: Optional[int] = Field(default=None, ge=0)


class GetMascotasResponse(BaseModel):
    mascotas: List[Mascota]


class DeleteMascotaResponse(BaseModel):
    message: str
