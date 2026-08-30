from pydantic import BaseModel, ConfigDict
from typing import Optional


class CategoriaBase(BaseModel):
    nombre: str
    estado: Optional[bool] = True


class CategoriaCreate(CategoriaBase):
    pass


class CategoriaUpdate(BaseModel):
    nombre: Optional[str] = None
    estado: Optional[bool] = None


class CategoriaResponse(CategoriaBase):
    id: int

    model_config = ConfigDict(from_attributes=True)