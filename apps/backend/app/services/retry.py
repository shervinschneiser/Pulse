from __future__ import annotations

from datetime import datetime, timedelta

from app.models.webhook_event import (
    WebhookEvent,
    WebhookEventStatus,
)


class RetryService:
    MAX_ATTEMPTS = 5

    @staticmethod
    def schedule_retry(event: WebhookEvent) -> None:
        event.attempts += 1

        if event.attempts >= RetryService.MAX_ATTEMPTS:
            event.status = WebhookEventStatus.DEAD
            event.next_retry_at = None
            return

        event.status = WebhookEventStatus.PENDING

        delay = 2**event.attempts

        event.next_retry_at = datetime.utcnow() + timedelta(
            seconds=delay,
        )
