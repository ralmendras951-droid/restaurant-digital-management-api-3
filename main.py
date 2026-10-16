from fastapi import FastAPI
from api.v1.router import router

app = FastAPI(
    title="Restaurant Management API",
    description="API REST para la gestión de productos de un menú digital",
    version="1.0.0"
)

app.include_router(router, prefix="/api/v1")


@app.get("/")
def root():
    return {
        "mensaje": "Restaurant Management API funcionando"
    }