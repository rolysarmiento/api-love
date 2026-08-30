from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.core.security import create_access_token


router = APIRouter(
    prefix="/api/auth",
    tags=["Autenticación"]
)


class LoginRequest(BaseModel):
    username: str
    password: str


@router.post("/token")
def login(data: LoginRequest):

    # Por ahora será temporal.
    # Luego lo conectaremos a usuarios si decidimos
    # implementar una tabla de administración.

    if data.username != "admin" or data.password != "1234":
        raise HTTPException(
            status_code=401,
            detail="Usuario o contraseña incorrectos"
        )

    token = create_access_token({
        "sub": data.username
    })

    return {
        "access_token": token,
        "token_type": "bearer"
    }


