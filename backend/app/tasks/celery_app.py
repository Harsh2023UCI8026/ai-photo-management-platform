from celery import Celery

celery_app = Celery(
    "photo_tasks",
    broker="redis://redis:6379/0",
    backend="redis://redis:6379/0"
)

import app.tasks.photo_tasks