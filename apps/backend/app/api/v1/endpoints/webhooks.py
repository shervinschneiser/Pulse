from uuid import UUID

from fastapi import APIRouter, Depends, Response, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.schemas.webhook import (
    WebhookCreate,
    WebhookRead,
    WebhookUpdate,
)
from app.services.webhook import WebhookService

router = APIRouter(prefix="/webhooks", tags=["Webhooks"])


@router.post(
    "",
    response_model=WebhookRead,
    status_code=status.HTTP_201_CREATED,
)
async def create_webhook(
    payload: WebhookCreate,
    db: AsyncSession = Depends(get_db),
):
    service = WebhookService(db)
    return await service.create(payload)


@router.get(
    "",
    response_model=list[WebhookRead],
)
async def list_webhooks(
    db: AsyncSession = Depends(get_db),
):
    service = WebhookService(db)
    return await service.list()


@router.get(
    "/{webhook_id}",
    response_model=WebhookRead,
)
async def get_webhook(
    webhook_id: UUID,
    db: AsyncSession = Depends(get_db),
):
    service = WebhookService(db)
    return await service.get(webhook_id)


@router.patch(
    "/{webhook_id}",
    response_model=WebhookRead,
)
async def update_webhook(
    webhook_id: UUID,
    payload: WebhookUpdate,
    db: AsyncSession = Depends(get_db),
):
    service = WebhookService(db)
    return await service.update(webhook_id, payload)


@router.delete(
    "/{webhook_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_webhook(
    webhook_id: UUID,
    db: AsyncSession = Depends(get_db),
):
    service = WebhookService(db)
    await service.delete(webhook_id)

    return Response(status_code=status.HTTP_204_NO_CONTENT)
