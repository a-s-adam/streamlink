"""Celery application configuration.

This module configures Celery for background task processing.
"""
from celery import Celery
from .config import get_settings

settings = get_settings()

# Create Celery app
celery_app = Celery(
    "streamlink",
    broker=settings.redis_url,
    backend=settings.redis_url,
    include=[
        "app.tasks.ingestion",
        "app.tasks.enrichment",
        "app.tasks.recommendations",
    ]
)

# Configure Celery
celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
    task_track_started=True,
    task_time_limit=30 * 60,  # 30 minutes
    task_soft_time_limit=25 * 60,  # 25 minutes
    worker_prefetch_multiplier=1,
    worker_max_tasks_per_child=1000,
)

# Optional: Configure task routes
celery_app.conf.task_routes = {
    "app.tasks.ingestion.*": {"queue": "ingestion"},
    "app.tasks.enrichment.*": {"queue": "enrichment"},
    "app.tasks.recommendations.*": {"queue": "recommendations"},
}

if __name__ == "__main__":
    celery_app.start()
