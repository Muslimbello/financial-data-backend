# celery.py
from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from django.conf import settings

# Set the default Django settings module
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.production")

app = Celery("stock_analysis")

# Use settings from Django
app.config_from_object("django.conf:settings", namespace="CELERY")

# Load tasks from all registered Django app configs
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)

# Configure Celery Beat schedule for periodic tasks
app.conf.beat_schedule = {
    "cleanup-old-data": {
        "task": "fetch_data.tasks.stock_tasks.cleanup_old_data_task",
        "schedule": 86400.0,  # Run daily
        "args": (730,),  # Keep 2 years of data
    }
}
