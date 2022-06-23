from __future__ import absolute_import, unicode_literals

import os

from celery import Celery
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tcpimage.settings')

app = Celery('tcpimage')
app.conf.enable_utc = False

app.conf.update(timezone='Europe/Moscow')

app.config_from_object(settings, namespace='CELERY')

app.autodiscover_tasks()


@app.task(bind=True)
def debug_task(self):
    print(f'request: {self.request!r}')


