from __future__ import annotations

import httpx
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import generate_signature
from app.models.webhook import Webhook
from app.models.webhook_event import WebhookEvent
from app.models.webhook_event import WebhookEventStatus
from app.services.retry import RetryService


class DeliveryService:
    def __init__(self, db: AsyncSession) -> None:
        self.db = db
        self.client = httpx.AsyncClient(timeout=10)

    async def deliver(
        self,
        webhook: Webhook,
        event: WebhookEvent,
    ) -> httpx.Response:
        signature = generate_signature(
            payload=event.payload_json.encode(),
            secret=webhook.secret,
        )

        headers = {
            "Content-Type": "application/json",
            "X-Pulse-Event": event.event_type,
            "X-Pulse-Signature": signature,
        }

        try:
            response = await self.client.post(
                webhook.target_url,
                json=event.payload,
                headers=headers,
            )

            event.response_status_code = response.status_code
            event.response_body = response.text

            if response.is_success:
                event.status = WebhookEventStatus.SUCCESS
                event.last_error = None
            else:
                event.status = WebhookEventStatus.FAILED
                event.last_error = response.text
                RetryService.schedule_retry(event)

        except Exception as exc:
            event.status = WebhookEventStatus.FAILED
            event.last_error = str(exc)
            event.response_status_code = None
            event.response_body = None

            RetryService.schedule_retry(event)
            raise

        finally:
            await self.db.commit()
            await self.db.refresh(event)

        return response

    async def close(self) -> None:
        await self.client.aclose()
