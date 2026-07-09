from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import AsyncSessionLocal
from app.services.webhook import WebhookService


async def get_db():
    async with AsyncSessionLocal() as session:
        yield session


DbSession = Annotated[AsyncSession, Depends(get_db)]


def get_webhook_service(db: DbSession) -> WebhookService:
    return WebhookService(db)


WebhookServiceDep = Annotated[
    WebhookService,
    Depends(get_webhook_service),
]
