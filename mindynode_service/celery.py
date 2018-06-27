# -*- coding: utf-8 -*-

from __future__ import absolute_import
import os
from celery import Celery
from django.conf import settings
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mindynode_service.settings')
app = Celery('mindynode_service')

app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)

# @app.on_after_configure.connect
# def setup_periodic_tasks(sender, **kwargs):
#     from .mindynode_nltk.tasks import task_update_feeds
#     sender.add_periodic_task(10.0, task_update_feeds.s(), name='update every 10 second')

app.conf.beat_schedule = {
  'update-feeds': {
    'task': 'mindynode_nltk.tasks.task_update_feeds',
    'schedule': crontab(hour='*/1')
  }
}