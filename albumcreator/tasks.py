# coding: utf-8
from datetime import timedelta
from celery.schedules import crontab
from celery.task import periodic_task

__author__ = 'edubecks'

from celery import task


@task
def add():
    print('Hello world')

CELERYBEAT_SCHEDULE = {
    'add-every-30-seconds': {
        'task': 'tasks.add',
        'schedule': timedelta(seconds=2),
        'args': (16, 16)
    },
}

