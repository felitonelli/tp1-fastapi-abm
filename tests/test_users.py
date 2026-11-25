def test_listar_todos(client):
    res = client.get("/user")
    assert res.status_code == 200
    assert len(res.json()["users"]) == 3


def test_listar_activos(client):
    res = client.get("/user", params={"is_active": True})
    usuarios = res.json()["users"]
    assert len(usuarios) == 2
    assert all(u["is_active"] for u in usuarios)


def test_listar_inactivos(client):
    res = client.get("/user", params={"is_active": False})
    usuarios = res.json()["users"]
    assert [u["name"] for u in usuarios] == ["ana gomez"]


def test_obtener_por_id(client):
    assert client.get("/user/1").json()["name"] == "juan perez"
    assert client.get("/user/99").status_code == 404


def test_crear_usuario(client):
    res = client.post("/user", json={"id": 10, "name": "nuevo"})
    assert res.status_code == 201
    assert client.get("/user/10").json()["is_active"] is True


def test_crear_usuario_id_repetido(client):
    res = client.post("/user", json={"id": 1, "name": "otro"})
    assert res.status_code == 409


def test_put_usuario(client):
    res = client.put("/user/1", json={"name": "juan p.", "is_active": False})
    assert res.status_code == 200
    assert res.json() == {"id": 1, "name": "juan p.", "is_active": False}


def test_put_usuario_incompleto(client):
    # PUT reemplaza todo: si falta un campo, 422
    assert client.put("/user/1", json={"name": "solo nombre"}).status_code == 422


def test_patch_usuario(client):
    res = client.patch("/user/2", json={"is_active": False})
    assert res.json() == {"id": 2, "name": "pepe sanchez", "is_active": False}
    res = client.patch("/user/2", json={"name": "pepe s."})
    assert res.json()["name"] == "pepe s."


def test_modificar_inexistente(client):
    assert client.put("/user/99", json={"name": "x", "is_active": True}).status_code == 404
    assert client.patch("/user/99", json={"name": "x"}).status_code == 404


def test_borrar_usuario(client):
    assert client.delete("/user/1").status_code == 200
    assert client.get("/user/1").status_code == 404
    assert client.delete("/user/1").status_code == 404
