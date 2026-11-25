from fastapi import FastAPI
from routers import users, mascotas

# Create the application instance
app = FastAPI(title="TP ABM de Usuarios y Mascotas")

# Router to user endpoints
app.include_router(users.router)
# Router de la entidad propia
app.include_router(mascotas.router)


# Define a GET route for the root URL
@app.get("/")
def read_root():
    mensaje = "TP ABM de Usuarios + Mascotas. Documentación en /docs"
    return {"message": mensaje}
