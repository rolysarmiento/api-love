from pydantic import BaseModel, ConfigDict
from typing import Optional


class FotoCreate(BaseModel):
    id_publicacion: int
    foto: str
    estado: Optional[bool] = True


class FotoUpdate(BaseModel):
    foto: Optional[str] = None
    estado: Optional[bool] = None


class FotoResponse(BaseModel):
    id: int
    id_publicacion: int
    foto: str
    estado: bool

    model_config = ConfigDict(
        from_attributes=True
    )