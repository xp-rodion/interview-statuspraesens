import os
import sys
from pathlib import Path

from celery import Celery
from django.conf import settings

app_path = Path(__file__).resolve().parent.parent / 'app'
sys.path.append(str(app_path))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.dev')

app = Celery('eroshiku_django')
app.config_from_object(settings, namespace='CELERY')

app.autodiscover_tasks()
