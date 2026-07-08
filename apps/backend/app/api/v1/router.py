from fastapi import APIRouter

from app.api.v1.endpoints.webhooks import router as webhooks_router

api_router = APIRouter()

api_router.include_router(webhooks_router)
