from pydantic import BaseModel, Field
from typing import List


class Restaurante(BaseModel):
    nombre: str = Field(..., min_length=1)
    direccion: str = Field(..., min_length=1)


class ProductoCreate(BaseModel):
    nombre: str = Field(..., min_length=1)
    descripcion: str = Field(..., min_length=1)
    precio: float = Field(..., gt=0)
    categoria: str = Field(..., min_length=1)
    disponible: bool
    calorias: int = Field(..., ge=0)
    ingredientes: List[str]
    restaurante: Restaurante