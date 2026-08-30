from sqlalchemy import (
    Column,
    Integer,
    String,
    Text,
    Boolean,
    DateTime,
    ForeignKey
)

from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from app.database.connection import Base


class Categoria(Base):
    __tablename__ = "categoria"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), nullable=False)
    estado = Column(Boolean, default=True)

    publicaciones = relationship(
        "Publicacion",
        back_populates="categoria"
    )


class Publicacion(Base):
    __tablename__ = "publicacion"

    id = Column(Integer, primary_key=True, index=True)
    url = Column(String(150), nullable=False, unique=True)
    titulo = Column(String(255), nullable=False)
    id_categoria = Column(
        Integer,
        ForeignKey("categoria.id"),
        nullable=False
    )
    comentarios = Column(Text)
    fecha_creacion = Column(
        DateTime,
        server_default=func.now()
    )
    estado = Column(Boolean, default=True)

    categoria = relationship(
        "Categoria",
        back_populates="publicaciones"
    )

    fotos = relationship(
        "Foto",
        back_populates="publicacion",
        cascade="all, delete-orphan"
    )


class Foto(Base):
    __tablename__ = "fotos"

    id = Column(Integer, primary_key=True, index=True)
    id_publicacion = Column(
        Integer,
        ForeignKey("publicacion.id", ondelete="CASCADE"),
        nullable=False
    )
    foto = Column(String(500), nullable=False)
    estado = Column(Boolean, default=True)

    publicacion = relationship(
        "Publicacion",
        back_populates="fotos"
    )