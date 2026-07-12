from __future__ import annotations

import asyncio
from datetime import UTC, datetime

from sqlalchemy import select

from app.core.celery import celery_app
from app.db.session import AsyncSessionLocal
from app.models.webhook_event import (
    WebhookEvent,
    WebhookEventStatus,
)
from app.workers.webhook import deliver_webhook


@celery_app.task(name="retry_pending_webhooks")
def retry_pending_webhooks() -> None:
    asyncio.run(_retry())


async def _retry() -> None:
    async with AsyncSessionLocal() as db:
        stmt = select(WebhookEvent).where(
            WebhookEvent.status == WebhookEventStatus.PENDING,
            WebhookEvent.next_retry_at.is_not(None),
            WebhookEvent.next_retry_at <= datetime.now(UTC),
        )

        result = await db.execute(stmt)

        events = result.scalars().all()

        for event in events:
            deliver_webhook.delay(
                str(event.webhook_id),
                str(event.id),
            )
