# from django.http import JsonResponse
# from .tasks import process_single_evtx_file

# def process_logs(request):
#     source = request.GET.get("source")

#     if source == "windows":
#         log_file_path = r'C:\Users\HP\Desktop\LoGs\Setup.evtx'
        
#         # Trigger Celery task for a single file
#         task_result = process_single_evtx_file.delay(log_file_path)

#         return JsonResponse({"message": "Log processing started.", "task_id": task_result.id})

#     return JsonResponse({"error": "Unsupported source"})
from django.http import JsonResponse
from .tasks import process_windows_event_logs
from celery.result import AsyncResult
from delivery_system.celery import app

def process_logs(request):
    source = request.GET.get("source")

    if source == "windows":
        log_types = request.GET.getlist("logs")  # e.g., ?logs=Application&logs=System
        if not log_types:
            log_types = ["Application", "System", "Setup", "Security"]

        # Start Celery task
        task = process_windows_event_logs.delay(log_types)

        return JsonResponse({
            "message": "Windows Event Log processing started.",
            "task_id": task.id
        })

    return JsonResponse({"error": "Unsupported source"})


def task_status(request, task_id):
    # Get the Celery task result
    result = AsyncResult(task_id, app=app)

    # Only include the result if task succeeded
    data = result.result if result.successful() else None

    # Optional: convert to JSON-serializable dict if needed
    if data:
        # Transform to only include severity_counts for front-end
        counts = {}
        for log_name, log_data in data.items():
            counts[log_name] = log_data.get("severity_counts", {})
        data = counts

    return JsonResponse({
        "state": result.state,
        "result": data,
    })

