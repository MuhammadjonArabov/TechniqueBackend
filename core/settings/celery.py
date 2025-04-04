from __future__ import absolute_import, unicode_literals
from celery.schedules import crontab

import os

from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings.base')

app = Celery('core',)

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()

app.conf.beat_schedule = {
    'update-usd-to-uzs-rate-every-24-hours': {
        'task': 'path.to.update_usd_to_uzs_rate',
        'schedule': crontab(minute=0, hour=0),
    },
}

app.conf.timezone = 'UTC'