from fastapi import FastAPI

from app.core.handlers import register_exception_handlers
from app.api.v1.router import api_router

app = FastAPI(
    title="Pulse",
    version="0.1.0",
)

register_exception_handlers(app)

app.include_router(api_router)


@app.get("/")
async def root() -> dict[str, str]:
    return {"message": "Pulse API"}


@app.get("/health")
async def health() -> dict[str, str]:
    return {"message": "OK"}
