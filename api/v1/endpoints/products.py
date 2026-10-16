from fastapi import APIRouter, HTTPException
from schemas.product import ProductoCreate
from core.database import productos_collection
from pymongo.errors import PyMongoError
from bson import ObjectId

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
            "id": str(resultado.inserted_id),
            "nombre": producto.nombre
        }

    except PyMongoError:
        raise HTTPException(
            status_code=500,
            detail="Error al registrar el producto"
        )
@router.get("/")
def listar_productos():

    try:
        productos = list(productos_collection.find())

        for producto in productos:
            producto["_id"] = str(producto["_id"])

        return productos

    except PyMongoError:
        raise HTTPException(
            status_code=500,
            detail="Error al listar los productos"
        )        
@router.get("/{producto_id}")
def obtener_producto(producto_id: str):

    try:
        producto = productos_collection.find_one(
            {"_id": ObjectId(producto_id)}
        )

        if not producto:
            raise HTTPException(
                status_code=404,
                detail="Producto no encontrado"
            )

        producto["_id"] = str(producto["_id"])

        return producto

    except PyMongoError:
        raise HTTPException(
            status_code=500,
            detail="Error al consultar el producto"
        )        