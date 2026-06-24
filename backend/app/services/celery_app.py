
from celery import Celery
from app.core.config import get_settings

settings = get_settings()

celery_app = Celery("ai_crm", broker=settings.REDIS_URL, backend=settings.REDIS_URL)
celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
    task_routes={
        "app.services.email_tasks.*": {"queue": "email"},
        "app.services.sync_tasks.*": {"queue": "sync"},
        "app.services.ai_tasks.*": {"queue": "ai"},
    },
)


@celery_app.task(name="app.services.email_tasks.send_email")
def send_email_task(to: str, subject: str, body: str):
    import logging
    logger = logging.getLogger(__name__)
    logger.info(f"Sending email to {to}: {subject}")
    return {"status": "sent", "to": to}


@celery_app.task(name="app.services.ai_tasks.retrain_model")
def retrain_model_task():
    import logging
    logger = logging.getLogger(__name__)
    logger.info("Model retraining started")
    return {"status": "retraining_started"}
