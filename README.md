# TP: ABM de Usuarios con FastAPI + ABM propio (Mascotas)

Extensión del proyecto `clase-fastapi` visto en clase:

- **Parte 1:** ABM completo de usuarios (alta, baja, modificación y listado con filtro por estado).
- **Parte 2:** ABM/CRUD de una entidad propia: **Mascota** (`id`, `nombre`, `especie`, `raza`, `edad`).

Mismo patrón que en clase: modelos con **Pydantic**, routers de **FastAPI** y almacenamiento **en memoria** (los datos se reinician cada vez que se levanta la app).

## Estructura

```
main.py              crea la app e incluye los routers
models/
  users.py           modelos Pydantic de usuario
  mascotas.py        modelos Pydantic de mascota
routers/
  users.py           endpoints /user
  mascotas.py        endpoints /mascotas
tests/               tests con pytest
```

## Instalar y levantar la aplicación

Requisitos: Python 3.12 o superior.

```bash
# 1. Crear el entorno virtual
python -m venv .venv

# 2. Activarlo
# Windows (PowerShell)
.venv\Scripts\Activate.ps1
# macOS / Linux
source .venv/bin/activate

# 3. Instalar dependencias
pip install -r requirements.txt

# 4. Levantar la API
fastapi dev main.py
```

La API queda en http://127.0.0.1:8000.

> En Windows, si `Activate.ps1` da error de "ejecución de scripts deshabilitada", correr antes:
> `Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass`

## Documentación interactiva (Swagger)

Con la API levantada, abrir **http://127.0.0.1:8000/docs**.

Ahí están todos los endpoints agrupados en **Usuarios** y **Mascotas**. Para probar uno: clic en el endpoint → **Try it out** → completar parámetros o body → **Execute**.

## Endpoints

### Parte 1 — Usuarios (`/user`)

| Método | Ruta | Descripción | Respuestas |
|---|---|---|---|
| GET | `/user` | Lista todos los usuarios | 200 |
| GET | `/user?is_active=true` | Solo activos | 200 |
| GET | `/user?is_active=false` | Solo inactivos | 200 |
| GET | `/user/{id}` | Un usuario por id | 200, 404 |
| POST | `/user` | Alta (`{"id": 4, "name": "...", "is_active": true}`) | 201, 409 si el id ya existe |
| PUT | `/user/{id}` | Modificación completa (`{"name": "...", "is_active": false}`) | 200, 404, 422 |
| PATCH | `/user/{id}` | Modificación parcial (solo los campos enviados) | 200, 404 |
| DELETE | `/user/{id}` | Baja | 200, 404 |

Datos de ejemplo: `juan perez` (activo), `pepe sanchez` (activo), `ana gomez` (inactiva).

### Parte 2 — Mascotas (`/mascotas`)

| Campo | Tipo | Detalle |
|---|---|---|
| `id` | int | Lo asigna la API al crear |
| `nombre` | str | |
| `especie` | str | perro, gato, etc. |
| `raza` | str | |
| `edad` | int | En años, no puede ser negativa (422) |

| Método | Ruta | Descripción | Respuestas |
|---|---|---|---|
| POST | `/mascotas` | Alta (`{"nombre": "Luna", "especie": "gato", "raza": "persa", "edad": 1}`) | 201, 422 |
| GET | `/mascotas` | Lista todas | 200 |
| GET | `/mascotas?especie=perro` | Filtra por especie (sin distinguir mayúsculas) | 200 |
| GET | `/mascotas?nombre=to` | Busca por parte del nombre | 200 |
| GET | `/mascotas?edad_max=5` | Mascotas de 5 años o menos | 200 |
| GET | `/mascotas/{id}` | Una mascota por id | 200, 404 |
| PUT | `/mascotas/{id}` | Modificación completa | 200, 404, 422 |
| PATCH | `/mascotas/{id}` | Modificación parcial (ej: `{"edad": 6}`) | 200, 404 |
| DELETE | `/mascotas/{id}` | Baja | 200, 404 |

Los filtros se pueden combinar: `/mascotas?especie=perro&edad_max=5`.

## Tests

Con el entorno virtual activado:

```bash
pytest
```
