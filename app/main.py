from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.routers import auth
from app.routers import categoria
from app.routers import publicacion
from app.routers import foto


app = FastAPI(
    title="API Love",
    description="API para publicaciones, categorías y fotos",
    version="1.0.0"
)


# =========================
# CORS
# =========================

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# =========================
# ROUTERS
# =========================

app.include_router(auth.router)
app.include_router(categoria.router)
app.include_router(publicacion.router)
app.include_router(foto.router)


# =========================
# ARCHIVOS
# =========================

app.mount(
    "/uploads",
    StaticFiles(directory="uploads"),
    name="uploads"
)


# =========================
# ROOT
# =========================

@app.get("/")
def root():
    return {
        "mensaje": "API Love funcionando"
    }