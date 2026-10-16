from fastapi import APIRouter
from api.v1.endpoints.products import router as products_router

router = APIRouter()

router.include_router(products_router)