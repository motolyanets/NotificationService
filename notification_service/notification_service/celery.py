import os
from celery import Celery
from celery.signals import setup_logging

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "notification_service.settings")
app = Celery("notification_service")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()


@setup_logging.connect
def config_loggers(*args, **kwargs) -> None:
    from logging.config import dictConfig
    from . import settings

    dictConfig(settings.LOGGING)
