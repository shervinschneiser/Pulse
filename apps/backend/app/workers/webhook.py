from __future__ import annotations

from uuid import UUID

from celery import shared_task
from sqlalchemy import select

from app.db.session import AsyncSessionLocal
from app.models.webhook import Webhook
from app.models.webhook_event import WebhookEvent
from app.services.delivery import DeliveryService


@shared_task(
    bind=True,
    autoretry_for=(),
)
def deliver_webhook(
    self,
    webhook_id: str,
    event_id: str,
) -> None:
    import asyncio

    asyncio.run(
        _deliver(
            UUID(webhook_id),
            UUID(event_id),
        )
    )


async def _deliver(
    webhook_id: UUID,
    event_id: UUID,
) -> None:
    async with AsyncSessionLocal() as db:
        webhook = await db.scalar(
            select(Webhook).where(
                Webhook.id == webhook_id,
            )
        )

        event = await db.scalar(
            select(WebhookEvent).where(
                WebhookEvent.id == event_id,
            )
        )

        if webhook is None or event is None:
            return

        service = DeliveryService(db)

        try:
            await service.deliver(
                webhook,
                event,
            )
        finally:
            await service.close()
