"""
This file configures celery.
"""

from __future__ import absolute_import
from celery import Celery

celery_app = Celery('app', broker='amqp://guest:guest@rabbitmq:5672', backend='rpc://', include=['app.tasks'])