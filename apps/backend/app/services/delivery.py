from __future__ import annotations

import httpx

from app.core.security import generate_signature
from app.models.webhook import Webhook
from app.models.webhook_event import WebhookEvent


class DeliveryService:
    def __init__(self) -> None:
        self.client = httpx.AsyncClient(timeout=10)

    async def deliver(
        self,
        webhook: Webhook,
        event: WebhookEvent,
    ) -> httpx.Response:
        payload = event.payload

        signature = generate_signature(
            payload=event.payload_json.encode(),
            secret=webhook.secret,
        )

        headers = {
            "Content-Type": "application/json",
            "X-Pulse-Event": event.event_type,
            "X-Pulse-Signature": signature,
        }

        response = await self.client.post(
            webhook.target_url,
            json=payload,
            headers=headers,
        )

        return response

    async def close(self) -> None:
        await self.client.aclose()
