NUEVA = {"nombre": "Luna", "especie": "gato", "raza": "persa", "edad": 1}


def test_crear_mascota_asigna_id(client):
    res = client.post("/mascotas", json=NUEVA)
    assert res.status_code == 201
    assert res.json() == {"id": 4, **NUEVA}


def test_crear_mascota_edad_negativa(client):
    res = client.post("/mascotas", json={**NUEVA, "edad": -1})
    assert res.status_code == 422


def test_listar_mascotas(client):
    assert len(client.get("/mascotas").json()["mascotas"]) == 3


def test_filtrar_por_especie_sin_mayusculas(client):
    res = client.get("/mascotas", params={"especie": "PERRO"})
    assert [m["nombre"] for m in res.json()["mascotas"]] == ["Toby", "Rocco"]


def test_filtrar_por_nombre_y_edad(client):
    res = client.get("/mascotas", params={"nombre": "o"})
    assert len(res.json()["mascotas"]) == 2  # Toby y Rocco
    res = client.get("/mascotas", params={"especie": "perro", "edad_max": 5})
    assert [m["nombre"] for m in res.json()["mascotas"]] == ["Toby"]


def test_obtener_mascota(client):
    assert client.get("/mascotas/2").json()["nombre"] == "Michi"
    assert client.get("/mascotas/99").status_code == 404


def test_put_mascota(client):
    res = client.put("/mascotas/1", json=NUEVA)
    assert res.json() == {"id": 1, **NUEVA}


def test_patch_mascota(client):
    res = client.patch("/mascotas/3", json={"edad": 10})
    assert res.json() == {"id": 3, "nombre": "Rocco", "especie": "perro", "raza": "labrador", "edad": 10}


def test_modificar_mascota_inexistente(client):
    assert client.put("/mascotas/99", json=NUEVA).status_code == 404
    assert client.patch("/mascotas/99", json={"edad": 3}).status_code == 404


def test_borrar_mascota(client):
    assert client.delete("/mascotas/2").status_code == 200
    assert client.get("/mascotas/2").status_code == 404
    assert client.delete("/mascotas/2").status_code == 404
