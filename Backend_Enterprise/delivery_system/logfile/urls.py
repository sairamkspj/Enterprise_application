from django.urls import path
from .views import LogFileUploadView   # make sure task_status exists in views.py
from .views_big_file import process_logs , task_status           # import your process_logs correctly

urlpatterns = [
    path('upload/', LogFileUploadView.as_view(), name='logfile-upload'),
    path('process-logs/', process_logs, name='process_logs'),   # unified naming
    path("task-status/<str:task_id>/", task_status, name="task_status"),
]
