import os
import uuid

from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    UploadFile,
    File,
    Form
)

from sqlalchemy.orm import Session

from app.database.connection import get_db
from app.database.models import Foto, Publicacion
from app.schemas.foto import FotoResponse


router = APIRouter(
    prefix="/fotos",
    tags=["Fotos"]
)


@router.post(
    "/",
    response_model=FotoResponse,
    status_code=201
)
async def subir_foto(
    id_publicacion: int = Form(...),
    foto: UploadFile = File(...),
    db: Session = Depends(get_db)
):

    # Verificar publicación
    publicacion = db.query(Publicacion).filter(
        Publicacion.id == id_publicacion
    ).first()

    if not publicacion:
        raise HTTPException(
            status_code=404,
            detail="La publicación no existe"
        )

    # Máximo 3 fotos
    cantidad_fotos = db.query(Foto).filter(
        Foto.id_publicacion == id_publicacion,
        Foto.estado == True
    ).count()

    if cantidad_fotos >= 3:
        raise HTTPException(
            status_code=400,
            detail="La publicación ya tiene el máximo de 3 fotos"
        )

    # Extensiones permitidas
    extensiones_permitidas = {
        ".jpg",
        ".jpeg",
        ".png",
        ".webp"
    }

    nombre_original = foto.filename or ""

    extension = os.path.splitext(
        nombre_original
    )[1].lower()

    if extension not in extensiones_permitidas:
        raise HTTPException(
            status_code=400,
            detail="Formato de imagen no permitido"
        )

    # Tipo MIME
    tipos_permitidos = {
        "image/jpeg",
        "image/png",
        "image/webp"
    }

    if foto.content_type not in tipos_permitidos:
        raise HTTPException(
            status_code=400,
            detail="El archivo no es una imagen válida"
        )

    # Crear carpeta
    carpeta = os.path.join(
        "uploads",
        "publicaciones",
        str(id_publicacion)
    )

    os.makedirs(
        carpeta,
        exist_ok=True
    )

    # Nombre único
    nombre_archivo = (
        f"{uuid.uuid4().hex}{extension}"
    )

    ruta_fisica = os.path.join(
        carpeta,
        nombre_archivo
    )

    # Guardar archivo
    contenido = await foto.read()

    with open(
        ruta_fisica,
        "wb"
    ) as archivo:
        archivo.write(contenido)

    # Ruta almacenada en BD
    ruta_bd = (
        f"/uploads/publicaciones/"
        f"{id_publicacion}/"
        f"{nombre_archivo}"
    )

    # Crear registro
    nueva_foto = Foto(
        id_publicacion=id_publicacion,
        foto=ruta_bd,
        estado=True
    )

    db.add(nueva_foto)
    db.commit()
    db.refresh(nueva_foto)

    return nueva_foto