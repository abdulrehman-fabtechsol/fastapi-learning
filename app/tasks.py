import time
from datetime import datetime
from celery import Celery
from sqlalchemy.orm import Session
from app.database import AsyncSessionLocal
from app import models

celery = Celery("tasks", broker="redis://redis:6379/0", backend="redis://redis:6379/0")

@celery.task
def create_user_message(user_id: int):
    """Create a message for a newly created user."""
    start_time = datetime.now()
    print(f"🟢 Task for user {user_id} started at {start_time}")

    db: Session = AsyncSessionLocal()
    
    for x in range(5):  # Simulate a delay in the task
        print(f"Task for user {user_id} is processing {x}...")
        time.sleep(10)

    try:
        new_message = models.Message(user_id=user_id, content="Welcome to our platform!")
        db.add(new_message)
        db.commit()
        print(f"✅ Message created for user {user_id}")
    finally:
        db.close()

    end_time = datetime.now()
    print(f"🔴 Task for user {user_id} finished at {end_time}")
