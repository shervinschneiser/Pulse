from __future__ import annotations

import enum

from sqlalchemy import Enum, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import BaseModel


class WebhookStatus(str, enum.Enum):
    ACTIVE = "active"
    DISABLED = "disabled"


class Webhook(BaseModel):
    __tablename__ = "webhooks"

    name: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    target_url: Mapped[str] = mapped_column(
        String(2048),
        nullable=False,
    )

    status: Mapped[WebhookStatus] = mapped_column(
        Enum(WebhookStatus, name="webhook_status"),
        default=WebhookStatus.ACTIVE,
        nullable=False,
    )

    secret: Mapped[str] = mapped_column(
        String(64),
        nullable=False,
        unique=True,
        index=True,
    )

    events = relationship(
        "WebhookEvent",
        back_populates="webhook",
        cascade="all, delete-orphan",
    )
