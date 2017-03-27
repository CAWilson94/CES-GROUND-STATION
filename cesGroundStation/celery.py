from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from django.conf import settings

# Setting celery config file to the Django settings file
os.environ.setdefault('DJANGO_SETTINGS_MODULE','cesGroundStation.settings')

# One instance of Celery created for our app
app = Celery('cesGroundStation')

# Celery config starts with "CELERY_" in django settings.py
app.config_from_object('django.conf:settings', namespace="CELERY")

# Tells celery to look for the tasks.py file in each app
# Alternatively the CELERY_IMPORTS setting has to be set
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)

@app.task(bind = True)
def debug_task(self):
	print('Request: {0!r}'.format(self.request))
