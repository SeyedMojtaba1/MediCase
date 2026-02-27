from __future__ import absolute_import, unicode_literals
from celery.schedules import crontab
from celery import Celery
import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'MediCaseBack.settings')

app = Celery('MediCaseBack')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
