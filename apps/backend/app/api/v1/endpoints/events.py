from uuid import UUID

from fastapi import APIRouter, Depends, status

from app.api.deps import (
    DBSessionDep,
    WebhookServiceDep,
)
from app.repositories.webhook_event import WebhookEventRepository
from app.schemas.webhook_event import (
    WebhookEventCreate,
    WebhookEventRead,
)
from app.tasks.delivery import deliver_webhook

router = APIRouter(
    prefix="/events",
    tags=["Events"],
)


@router.post(
    "",
    response_model=WebhookEventRead,
    status_code=status.HTTP_201_CREATED,
)
async def publish_event(
    payload: WebhookEventCreate,
    db: DBSessionDep = Depends(DBSessionDep),
    webhook_service: WebhookServiceDep = Depends(WebhookServiceDep),
):
    webhook = await webhook_service.get(payload.webhook_id)

    repository = WebhookEventRepository(db)

    event = await repository.create(payload)

    deliver_webhook.delay(
        str(webhook.id),
        str(event.id),
    )

    return event
