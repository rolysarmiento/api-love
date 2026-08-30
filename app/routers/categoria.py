from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.connection import get_db
from app.database.models import Categoria
from app.schemas.categoria import (
    CategoriaCreate,
    CategoriaUpdate,
    CategoriaResponse
)

router = APIRouter(
    prefix="/categorias",
    tags=["Categorías"]
)


@router.post(
    "/",
    response_model=CategoriaResponse,
    status_code=201
)
def crear_categoria(
    categoria: CategoriaCreate,
    db: Session = Depends(get_db)
):

    nueva_categoria = Categoria(
        nombre=categoria.nombre,
        estado=categoria.estado
    )

    db.add(nueva_categoria)
    db.commit()
    db.refresh(nueva_categoria)

    return nueva_categoria


@router.get(
    "/",
    response_model=list[CategoriaResponse]
)
def listar_categorias(
    db: Session = Depends(get_db)
):

    return db.query(Categoria).all()


@router.get(
    "/{id}",
    response_model=CategoriaResponse
)
def obtener_categoria(
    id: int,
    db: Session = Depends(get_db)
):

    categoria = db.query(Categoria).filter(
        Categoria.id == id
    ).first()

    if not categoria:
        raise HTTPException(
            status_code=404,
            detail="Categoría no encontrada"
        )

    return categoria


@router.put(
    "/{id}",
    response_model=CategoriaResponse
)
def actualizar_categoria(
    id: int,
    datos: CategoriaUpdate,
    db: Session = Depends(get_db)
):

    categoria = db.query(Categoria).filter(
        Categoria.id == id
    ).first()

    if not categoria:
        raise HTTPException(
            status_code=404,
            detail="Categoría no encontrada"
        )

    if datos.nombre is not None:
        categoria.nombre = datos.nombre

    if datos.estado is not None:
        categoria.estado = datos.estado

    db.commit()
    db.refresh(categoria)

    return categoria


@router.delete("/{id}")
def eliminar_categoria(
    id: int,
    db: Session = Depends(get_db)
):

    categoria = db.query(Categoria).filter(
        Categoria.id == id
    ).first()

    if not categoria:
        raise HTTPException(
            status_code=404,
            detail="Categoría no encontrada"
        )

    db.delete(categoria)
    db.commit()

    return {
        "mensaje": "Categoría eliminada correctamente"
    }