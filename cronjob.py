from celery_app import celery

@celery.task
def my_scheduled_task():
    """This runs periodically as per schedule."""
    print("✅ Running scheduled task")
