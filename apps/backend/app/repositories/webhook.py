from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.webhook import Webhook
from app.schemas.webhook import WebhookCreate, WebhookUpdate


class WebhookRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, data: WebhookCreate) -> Webhook:
        webhook = Webhook(**data.model_dump())

        self.db.add(webhook)
        await self.db.commit()
        await self.db.refresh(webhook)

        return webhook

    async def get(self, webhook_id: UUID) -> Webhook | None:
        stmt = select(Webhook).where(Webhook.id == webhook_id)

        result = await self.db.execute(stmt)

        return result.scalar_one_or_none()

    async def list(self) -> list[Webhook]:
        stmt = select(Webhook).order_by(Webhook.created_at.desc())

        result = await self.db.execute(stmt)

        return list(result.scalars().all())

    async def update(
        self,
        webhook: Webhook,
        data: WebhookUpdate,
    ) -> Webhook:
        values = data.model_dump(exclude_unset=True)

        for key, value in values.items():
            setattr(webhook, key, value)

        await self.db.commit()
        await self.db.refresh(webhook)

        return webhook

    async def delete(self, webhook: Webhook) -> None:
        await self.db.delete(webhook)
        await self.db.commit()
