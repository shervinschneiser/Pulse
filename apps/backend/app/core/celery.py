from celery import Celery

from app.core.config import get_settings

settings = get_settings()

celery_app = Celery(
    "pulse",
    broker=settings.redis_url,
    backend=settings.redis_url,
)

celery_app.conf.update(
    task_serializer="json",
    result_serializer="json",
    accept_content=["json"],
    timezone="UTC",
    enable_utc=True,
    beat_schedule={
        "retry-pending-webhooks": {
            "task": "retry_pending_webhooks",
            "schedule": 30.0,
        },
    },
)

celery_app.autodiscover_tasks(
    [
        "app.workers",
    ]
)
