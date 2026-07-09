from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.webhook_event import WebhookEvent
from app.schemas.webhook_event import WebhookEventCreate


class WebhookEventRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(
        self,
        data: WebhookEventCreate,
    ) -> WebhookEvent:
        event = WebhookEvent(**data.model_dump())

        self.db.add(event)

        await self.db.commit()
        await self.db.refresh(event)

        return event

    async def list_pending(self) -> list[WebhookEvent]:
        stmt = (
            select(WebhookEvent)
            .where(WebhookEvent.status == "pending")
            .order_by(WebhookEvent.created_at)
        )

        result = await self.db.execute(stmt)

        return list(result.scalars().all())
