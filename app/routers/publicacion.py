from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.connection import get_db
from app.database.models import Publicacion, Categoria

from app.schemas.publicacion import (
    PublicacionCreate,
    PublicacionUpdate,
    PublicacionResponse
)


router = APIRouter(
    prefix="/publicaciones",
    tags=["Publicaciones"]
)


# =========================================================
# CREAR PUBLICACIÓN
# =========================================================

@router.post(
    "/",
    response_model=PublicacionResponse,
    status_code=201
)
def crear_publicacion(
    publicacion: PublicacionCreate,
    db: Session = Depends(get_db)
):

    # Validar categoría
    categoria = db.query(Categoria).filter(
        Categoria.id == publicacion.id_categoria
    ).first()

    if not categoria:
        raise HTTPException(
            status_code=400,
            detail="La categoría no existe"
        )

    # Validar URL única
    existe = db.query(Publicacion).filter(
        Publicacion.url == publicacion.url
    ).first()

    if existe:
        raise HTTPException(
            status_code=409,
            detail="La URL ya está registrada"
        )

    nueva_publicacion = Publicacion(
        url=publicacion.url,
        titulo=publicacion.titulo,
        id_categoria=publicacion.id_categoria,
        comentarios=publicacion.comentarios,
        estado=publicacion.estado
    )

    db.add(nueva_publicacion)
    db.commit()
    db.refresh(nueva_publicacion)

    return nueva_publicacion


# =========================================================
# LISTAR PUBLICACIONES
# =========================================================

@router.get(
    "/",
    response_model=list[PublicacionResponse]
)
def listar_publicaciones(
    db: Session = Depends(get_db)
):

    return db.query(Publicacion).all()


# =========================================================
# OBTENER PUBLICACIÓN
# =========================================================

@router.get(
    "/{url}",
    response_model=PublicacionResponse
)
def obtener_publicacion(
    url: str,
    db: Session = Depends(get_db)
):

    publicacion = db.query(Publicacion).filter(
        Publicacion.url == url
    ).first()

    if not publicacion:
        raise HTTPException(
            status_code=404,
            detail="Publicación no encontrada"
        )

    return publicacion


# =========================================================
# ACTUALIZAR PUBLICACIÓN
# =========================================================

@router.put(
    "/{id}",
    response_model=PublicacionResponse
)
def actualizar_publicacion(
    id: int,
    datos: PublicacionUpdate,
    db: Session = Depends(get_db)
):

    publicacion = db.query(Publicacion).filter(
        Publicacion.id == id
    ).first()

    if not publicacion:
        raise HTTPException(
            status_code=404,
            detail="Publicación no encontrada"
        )

    # -----------------------------------------
    # Validar categoría
    # -----------------------------------------

    if datos.id_categoria is not None:

        categoria = db.query(Categoria).filter(
            Categoria.id == datos.id_categoria
        ).first()

        if not categoria:
            raise HTTPException(
                status_code=400,
                detail="La categoría no existe"
            )

        publicacion.id_categoria = datos.id_categoria


    # -----------------------------------------
    # Validar URL única
    # -----------------------------------------

    if datos.url is not None:

        existe = db.query(Publicacion).filter(
            Publicacion.url == datos.url,
            Publicacion.id != id
        ).first()

        if existe:
            raise HTTPException(
                status_code=409,
                detail="La URL ya está registrada"
            )

        publicacion.url = datos.url


    # -----------------------------------------
    # Actualizar datos
    # -----------------------------------------

    if datos.titulo is not None:
        publicacion.titulo = datos.titulo

    if datos.comentarios is not None:
        publicacion.comentarios = datos.comentarios

    if datos.estado is not None:
        publicacion.estado = datos.estado


    db.commit()
    db.refresh(publicacion)

    return publicacion


# =========================================================
# ELIMINAR PUBLICACIÓN
# =========================================================

@router.delete("/{id}")
def eliminar_publicacion(
    id: int,
    db: Session = Depends(get_db)
):

    publicacion = db.query(Publicacion).filter(
        Publicacion.id == id
    ).first()

    if not publicacion:
        raise HTTPException(
            status_code=404,
            detail="Publicación no encontrada"
        )

    db.delete(publicacion)
    db.commit()

    return {
        "mensaje": "Publicación eliminada correctamente"
    }