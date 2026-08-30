from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime


class FotoPublicacionResponse(BaseModel):
    id: int
    foto: str
    estado: bool

    model_config = ConfigDict(
        from_attributes=True
    )


class PublicacionBase(BaseModel):
    url: str
    titulo: str
    id_categoria: int
    comentarios: Optional[str] = None
    estado: Optional[bool] = True


class PublicacionCreate(PublicacionBase):
    pass


class PublicacionUpdate(BaseModel):
    url: Optional[str] = None
    titulo: Optional[str] = None
    id_categoria: Optional[int] = None
    comentarios: Optional[str] = None
    estado: Optional[bool] = None


class PublicacionResponse(PublicacionBase):
    id: int
    fecha_creacion: datetime
    fotos: list[FotoPublicacionResponse] = []

    model_config = ConfigDict(
        from_attributes=True
    )