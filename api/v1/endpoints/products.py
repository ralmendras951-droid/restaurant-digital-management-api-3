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
@router.put("/{producto_id}")
def actualizar_producto(producto_id: str, producto: ProductoCreate):

    try:
        producto_data = producto.model_dump()

        resultado = productos_collection.update_one(
            {"_id": ObjectId(producto_id)},
            {"$set": producto_data}
        )

        if resultado.matched_count == 0:
            raise HTTPException(
                status_code=404,
                detail="Producto no encontrado"
            )

        return {
            "mensaje": "Producto actualizado correctamente",
            "id": producto_id,
            "nombre": producto.nombre
        }

    except PyMongoError:
        raise HTTPException(
            status_code=500,
            detail="Error al actualizar el producto"
        )              
@router.delete("/{producto_id}")
def eliminar_producto(producto_id: str):

    try:
        resultado = productos_collection.delete_one(
            {"_id": ObjectId(producto_id)}
        )

        if resultado.deleted_count == 0:
            raise HTTPException(
                status_code=404,
                detail="Producto no encontrado"
            )

        return {
            "mensaje": "Producto eliminado correctamente",
            "id": producto_id
        }

    except PyMongoError:
        raise HTTPException(
            status_code=500,
            detail="Error al eliminar el producto"
        )
@router.get("/buscar/nombre/{nombre}")
def buscar_por_nombre(nombre: str):

    try:
        productos = list(
            productos_collection.find(
                {"nombre": {"$regex": nombre, "$options": "i"}}
            )
        )

        for producto in productos:
            producto["_id"] = str(producto["_id"])

        return productos

    except PyMongoError:
        raise HTTPException(
            status_code=500,
            detail="Error al buscar productos por nombre"
        )
        

@router.get("/filtrar/categoria/{categoria}")
def filtrar_por_categoria(categoria: str):

    try:
        productos = list(
            productos_collection.find(
                {"categoria": {"$regex": f"^{categoria}$", "$options": "i"}}
            )
        )

        for producto in productos:
            producto["_id"] = str(producto["_id"])

        return productos

    except PyMongoError:
        raise HTTPException(
            status_code=500,
            detail="Error al filtrar productos por categoría"
        )


@router.get("/filtrar/precio/{precio}")
def filtrar_por_precio(precio: float):

    try:
        productos = list(
            productos_collection.find(
                {"precio": {"$lte": precio}}
            )
        )

        for producto in productos:
            producto["_id"] = str(producto["_id"])

        return productos

    except PyMongoError:
        raise HTTPException(
            status_code=500,
            detail="Error al filtrar productos por precio"
        )
@router.get("/filtrar/disponibles")
def filtrar_disponibles():

    try:
        productos = list(
            productos_collection.find(
                {"disponible": True}
            )
        )

        for producto in productos:
            producto["_id"] = str(producto["_id"])

        return productos

    except PyMongoError:
        raise HTTPException(
            status_code=500,
            detail="Error al filtrar productos disponibles"
        )        