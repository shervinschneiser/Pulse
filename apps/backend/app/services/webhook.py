from uuid import UUID

from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.webhook import Webhook
from app.repositories.webhook import WebhookRepository
from app.schemas.webhook import WebhookCreate, WebhookUpdate


class WebhookService:
    def __init__(self, db: AsyncSession):
        self.repository = WebhookRepository(db)

    async def create(self, data: WebhookCreate) -> Webhook:
        return await self.repository.create(data)

    async def list(self) -> list[Webhook]:
        return await self.repository.list()

    async def get(self, webhook_id: UUID) -> Webhook:
        webhook = await self.repository.get(webhook_id)

        if webhook is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Webhook not found",
            )

        return webhook

    async def update(
        self,
        webhook_id: UUID,
        data: WebhookUpdate,
    ) -> Webhook:
        webhook = await self.get(webhook_id)

        return await self.repository.update(webhook, data)

    async def delete(self, webhook_id: UUID) -> None:
        webhook = await self.get(webhook_id)

        await self.repository.delete(webhook)
