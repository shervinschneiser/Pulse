from uuid import UUID

from fastapi import APIRouter, Depends, Response, status

from app.api.deps import WebhookServiceDep
from app.schemas.webhook import (
    WebhookCreate,
    WebhookRead,
    WebhookUpdate,
)

router = APIRouter(prefix="/webhooks", tags=["Webhooks"])


@router.post(
    "",
    response_model=WebhookRead,
    status_code=status.HTTP_201_CREATED,
)
async def create_webhook(
    payload: WebhookCreate,
    service: WebhookServiceDep = Depends(WebhookServiceDep),
):
    return await service.create(payload)


@router.get(
    "",
    response_model=list[WebhookRead],
)
async def list_webhooks(
    service: WebhookServiceDep = Depends(WebhookServiceDep),
):
    return await service.list()


@router.get(
    "/{webhook_id}",
    response_model=WebhookRead,
)
async def get_webhook(
    webhook_id: UUID,
    service: WebhookServiceDep = Depends(WebhookServiceDep),
):
    return await service.get(webhook_id)


@router.patch(
    "/{webhook_id}",
    response_model=WebhookRead,
)
async def update_webhook(
    webhook_id: UUID,
    payload: WebhookUpdate,
    service: WebhookServiceDep = Depends(WebhookServiceDep),
):
    return await service.update(webhook_id, payload)


@router.delete(
    "/{webhook_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_webhook(
    webhook_id: UUID,
    service: WebhookServiceDep = Depends(WebhookServiceDep),
):
    await service.delete(webhook_id)

    return Response(status_code=status.HTTP_204_NO_CONTENT)
