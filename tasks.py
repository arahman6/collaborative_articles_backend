from celery.schedules import crontab
from celery_worker import celery, generate_daily_articles

# Schedule the task to run daily at midnight
celery.conf.beat_schedule = {
    "generate_articles_every_day": {
        "task": "celery_worker.generate_daily_articles",
        "schedule": crontab(hour=0, minute=0),  # Runs at 00:00 daily
    }
}
