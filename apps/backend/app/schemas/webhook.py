from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, HttpUrl


class WebhookBase(BaseModel):
    url: HttpUrl
    description: str | None = None
    is_active: bool = True


class WebhookCreate(WebhookBase):
    pass


class WebhookUpdate(BaseModel):
    url: HttpUrl | None = None
    description: str | None = None
    is_active: bool | None = None


class WebhookRead(WebhookBase):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    created_at: datetime
    updated_at: datetime
