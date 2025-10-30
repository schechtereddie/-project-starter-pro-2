from celery import Celery
from backend.app.core.config import settings

celery = Celery("psp")
celery.conf.broker_url = settings.CELERY_BROKER_URL
celery.conf.result_backend = settings.CELERY_RESULT_BACKEND

@celery.task
def test_task():
    return "Celery running OK"

