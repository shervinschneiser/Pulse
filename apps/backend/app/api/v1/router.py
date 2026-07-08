from fastapi import APIRouter

from app.api.v1.endpoints import webhook_router

api_router = APIRouter(prefix="/api/v1")

api_router.include_router(webhook_router)
