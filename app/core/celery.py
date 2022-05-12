from celery import Celery

from app.config import settings

print(settings.CELERY_BROKER)
celery_config = {
    "broker_url": settings.CELERY_BROKER,
    "result_expires": 7200,  # in secs
    "worker_prefetch_multiplier": 1,
    "result_backend": settings.CELERY_BACKEND,
}

celery_app = Celery("worker", config_source=celery_config)


celery_app.conf.task_routes = {
    "app.worker.task.task": {"queue": "some-function"},
}

celery_app.conf.update(
    task_track_started=True,
    task_serializer="pickle",
    accept_content=["json", "pickle"],
)

