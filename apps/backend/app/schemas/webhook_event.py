from datetime import datetime
from uuid import UUID

from pydantic import BaseModel

from app.models.webhook_event import WebhookEventStatus


class WebhookEventCreate(BaseModel):
    webhook_id: UUID
    event_type: str
    payload: dict


class WebhookEventRead(BaseModel):
    id: UUID
    webhook_id: UUID
    event_type: str
    payload: dict
    status: WebhookEventStatus
    attempts: int
    next_retry_at: datetime | None
    last_error: str | None
    created_at: datetime

    model_config = {
        "from_attributes": True,
    }
