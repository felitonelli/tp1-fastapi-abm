import pytest
from fastapi.testclient import TestClient

from main import app
from routers import mascotas, users


@pytest.fixture(autouse=True)
def datos_limpios():
    # Los datos viven en memoria: cada test arranca con la lista original
    usuarios_orig = [u.model_copy() for u in users.usuarios]
    mascotas_orig = [m.model_copy() for m in mascotas.mascotas]
    yield
    users.usuarios[:] = usuarios_orig
    mascotas.mascotas[:] = mascotas_orig


@pytest.fixture
def client():
    return TestClient(app)
