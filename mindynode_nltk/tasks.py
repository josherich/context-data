from __future__ import absolute_import
from celery.task.schedules import crontab
from celery.decorators import periodic_task
from celery.task import task
from celery.utils.log import get_task_logger

from mindynode_service.celery import app
from mindynode_nltk.functions import update_feeds

import logging
logger = get_task_logger(__name__)

params = [
  ['zh_tech', 'zh'],
  ['zh_economics', 'zh'],
  ['en_general', 'en'],
  ['en_tech', 'en'],
  ['china', 'zh'],
]

@app.task
def task_update_feeds():
  for param in params:
    update_feeds(param[0])

@app.task
def task_build_group_today_pages():
  pass

@app.task
def task_build_today_bow():
  pass

@app.task
def task_build_group_history_pages():
  pass
