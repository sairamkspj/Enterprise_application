# import os
# from celery import Celery

# # Set the default Django settings module for the 'celery' program.
# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'delivery_system.settings')

# # Create the Celery application instance
# app = Celery('delivery_system')

# # Using a string here means the worker doesn't have to serialize
# # the configuration object to child processes.
# # - namespace='CELERY' means all celery-related configuration keys
# #   should have a `CELERY_` prefix.
# app.config_from_object('django.conf:settings', namespace='CELERY')

# # Load task modules from all registered Django apps.
# app.autodiscover_tasks()

# @app.task(bind=True, ignore_result=True)
# def debug_task(self):
#     print(f'Request: {self.request!r}')

# import os
# from celery import Celery

# os.environ.setdefault("DJANGO_SETTINGS_MODULE", "delivery_system.settings")

# app = Celery("delivery_system")

# # Load task modules from all registered Django apps
# app.config_from_object("django.conf:settings", namespace="CELERY")
# app.autodiscover_tasks()

import os
from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "delivery_system.settings")

app = Celery(
    'delivery_system',
    broker='redis://127.0.0.1:6379/0',   # Redis broker
    backend='redis://127.0.0.1:6379/0',  # Redis backend
)

app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()

