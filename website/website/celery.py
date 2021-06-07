import logging
import os

from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'website.settings')

app = Celery('website', broker='redis://localhost:6379/')
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()
logger = logging.getLogger(__name__)

app.conf.beat_schedule = {
    "check_available_products": {
        "task": "market.task.make_5_percent_discount",
        "schedule": crontab()
    },
}
