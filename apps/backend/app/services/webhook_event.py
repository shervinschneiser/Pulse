from uuid import UUID

from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.webhook_event import WebhookEvent
from app.repositories.webhook_event import WebhookEventRepository
from app.schemas.webhook_event import WebhookEventCreate


class WebhookEventService:
    def __init__(self, db: AsyncSession):
        self.repository = WebhookEventRepository(db)

    async def create(
        self,
        data: WebhookEventCreate,
    ) -> WebhookEvent:
        return await self.repository.create(data)

    async def list_pending(self) -> list[WebhookEvent]:
        return await self.repository.list_pending()

    async def get(
        self,
        event_id: UUID,
    ) -> WebhookEvent:
        events = await self.repository.list_pending()

        for event in events:
            if event.id == event_id:
                return event

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Webhook event not found",
        )
