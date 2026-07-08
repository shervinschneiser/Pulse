from fastapi import FastAPI

from app.api.v1.router import api_router

app = FastAPI(
    title="Pulse",
    version="0.1.0",
)

app.include_router(api_router)


@app.get("/")
async def root() -> dict[str, str]:
    return {"message": "Pulse API"}


@app.get("/health")
async def health() -> dict[str, str]:
    return {"message": "OK"}
