from celery import Celery

celery = Celery("tasks", broker="redis://redis:6379/0", backend="redis://redis:6379/0")

celery.conf.update(
    task_serializer="json",
    imports=["app.tasks", "cronjob"],
    worker_prefetch_multiplier=1,  # Ensures tasks are distributed evenly
    task_acks_late=True  # Ensures tasks are not lost if a worker crashes
)
