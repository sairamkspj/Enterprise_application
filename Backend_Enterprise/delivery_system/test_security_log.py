from logfile.tasks import process_windows_event_logs

result = process_windows_event_logs.delay(["Security", "System", "Application"])
print(result.get(timeout=10))
