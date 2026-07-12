from fastapi import APIRouter

from app.api.v1.endpoints import (
    event_router,
    webhook_router,
)

api_router = APIRouter(prefix="/api/v1")

api_router.include_router(webhook_router)
api_router.include_router(event_router)
