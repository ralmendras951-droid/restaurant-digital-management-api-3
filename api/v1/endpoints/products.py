from fastapi import APIRouter, HTTPException
from schemas.product import ProductoCreate
from core.database import productos_collection
from pymongo.errors import PyMongoError

router = APIRouter(
    prefix="/productos",
    tags=["Productos"]
)


@router.post("/", status_code=201)
def registrar_producto(producto: ProductoCreate):

    try:
        producto_data = producto.model_dump()

        resultado = productos_collection.insert_one(producto_data)

        return {
            "mensaje": "Producto registrado correctamente",
            "id": str(resultado.inserted_id)
        }

    except PyMongoError:
        raise HTTPException(
            status_code=500,
            detail="Error al registrar el producto"
        )