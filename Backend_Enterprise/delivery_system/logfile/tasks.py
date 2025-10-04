
# import logging
# from celery import shared_task
# import win32evtlog

# logger = logging.getLogger(__name__)

# SEVERITY_MAP = {
#     1: "Critical",
#     2: "Error",
#     3: "Warning",
#     4: "Information",
#     0: "Information"  # default
# }

# @shared_task(time_limit=3600)
# def process_windows_event_logs(log_types=None):
#     """
#     Process Windows Event Viewer logs dynamically.
#     log_types: list of logs to process, e.g., ["Application", "System", "Setup"]
#     """
#     if log_types is None:
#         log_types = ["Application", "System", "Setup"]

#     results = {}

#     for log_name in log_types:
#         try:
#             server = "localhost"  # local machine
#             handle = win32evtlog.OpenEventLog(server, log_name)
#             total = win32evtlog.GetNumberOfEventLogRecords(handle)

#             severity_counts = {"Critical": 0, "Error": 0, "Warning": 0, "Information": 0, "Unknown": 0}
#             flags = win32evtlog.EVENTLOG_BACKWARDS_READ | win32evtlog.EVENTLOG_SEQUENTIAL_READ

#             while True:
#                 # //The variable events is a list that contains Python objects, with each object representing a single entry from the Windows Event Log.
#                 # read byte code and return It understands the log's structure and extracts attributes like Event ID, Event Type, and the log message. It then places this data into a Python object for each event.
#                 events = win32evtlog.ReadEventLog(handle, flags, 0)
#                 if not events:
#                     break

#                 for e in events:
#                     level = getattr(e, "EventType", 0)
#                     # Map EventType to severity
#                     if level == win32evtlog.EVENTLOG_ERROR_TYPE:
#                         severity_counts["Error"] += 1
#                     elif level == win32evtlog.EVENTLOG_WARNING_TYPE:
#                         severity_counts["Warning"] += 1
#                     elif level == win32evtlog.EVENTLOG_INFORMATION_TYPE:
#                         severity_counts["Information"] += 1
#                     else:
#                         severity_counts["Unknown"] += 1

#             results[log_name] = severity_counts
#             win32evtlog.CloseEventLog(handle)

#         except Exception as ex:
#             logger.error(f"Failed to process {log_name}: {ex}")
#             results[log_name] = {"error": str(ex)}

#     return results



# # win32evtlog.EVENTLOG_ERROR_TYPE: Corresponds to the integer 1.

# # win32evtlog.EVENTLOG_WARNING_TYPE: Corresponds to the integer 2.

# # win32evtlog.EVENTLOG_INFORMATION_TYPE: Corresponds to the integer 4.

# # win32evtlog.EVENTLOG_AUDIT_SUCCESS: Corresponds to the integer 8.

# # win32evtlog.EVENTLOG_AUDIT_FAILURE: Corresponds to the integer 16.
# import logging
# from celery import shared_task
# import win32evtlog
# import win32security, win32api
# import ntsecuritycon as con
# from win32 import win32evtlog as wevt  # modern winevt API

# logger = logging.getLogger(__name__)

# # ------------------------
# # Enable SeSecurityPrivilege
# # ------------------------
# def enable_privilege(priv):
#     try:
#         flags = con.SE_PRIVILEGE_ENABLED
#         htoken = win32security.OpenProcessToken(
#             win32api.GetCurrentProcess(),
#             con.TOKEN_ADJUST_PRIVILEGES | con.TOKEN_QUERY
#         )
#         luid = win32security.LookupPrivilegeValue(None, priv)
#         win32security.AdjustTokenPrivileges(htoken, 0, [(luid, flags)])
#         logger.info(f"Privilege enabled: {priv}")
#     except Exception as e:
#         logger.warning(f"Could not enable privilege {priv}: {e}")

# # ------------------------
# # Celery task
# # ------------------------
# @shared_task(time_limit=3600)
# def process_windows_event_logs(log_types=None):
#     if log_types is None:
#         log_types = ["Application", "System", "Setup", "Security"]

#     results = {}

#     # EventType → severity mapping for win32evtlog
#     severity_map = {
#         win32evtlog.EVENTLOG_ERROR_TYPE: "Error",
#         win32evtlog.EVENTLOG_WARNING_TYPE: "Warning",
#         win32evtlog.EVENTLOG_INFORMATION_TYPE: "Information"
#     }

#     for log_name in log_types:
#         try:
#             # ------------------------
#             # Security log handled by winevt.EvtQuery
#             # ------------------------
#             if log_name == "Security":
#                 enable_privilege(win32security.SE_SECURITY_NAME)
#                 query = "*[System]"
#                 handle = wevt.EvtQuery("Security", wevt.EvtQueryChannelPath, query)

#                 severity_counts = {"Audit Success": 0, "Audit Failure": 0, "Unknown": 0}
#                 total = 0

#                 while True:
#                     events = wevt.EvtNext(handle, 10)
#                     if not events:
#                         break
#                     total += len(events)

#                     for e in events:
#                         xml = wevt.EvtRender(e, wevt.EvtRenderEventXml)
#                         if "Audit Success" in xml:
#                             severity_counts["Audit Success"] += 1
#                         elif "Audit Failure" in xml:
#                             severity_counts["Audit Failure"] += 1
#                         else:
#                             severity_counts["Unknown"] += 1

#                 results[log_name] = {"total_records": total, "severity_counts": severity_counts}

#             # ------------------------
#             # Application/System/Setup handled by win32evtlog
#             # ------------------------
#             else:
#                 server = "localhost"
#                 handle = win32evtlog.OpenEventLog(server, log_name)
#                 # gives the number of records in log
#                 total = win32evtlog.GetNumberOfEventLogRecords(handle)


#                 severity_counts = {"Critical": 0, "Error": 0, "Warning": 0, "Information": 0, "Unknown": 0}
#                 flags = win32evtlog.EVENTLOG_BACKWARDS_READ | win32evtlog.EVENTLOG_SEQUENTIAL_READ

#                 while True:
#                     events = win32evtlog.ReadEventLog(handle, flags, 0)
#                     # return EventID → the ID of the event EventType → Error, Warning, Info TimeGenerated → timestamp SourceName → where it came from Strings → any message text how
#                     if not events:
#                         break

#                     for e in events:
#                         level = getattr(e, "EventType", 0)
#                         severity = severity_map.get(level, "Unknown")
#                         severity_counts[severity] += 1

#                 results[log_name] = {"total_records": total, "severity_counts": severity_counts}
#                 win32evtlog.CloseEventLog(handle)

#         except Exception as ex:
#             logger.error(f"Failed to process {log_name}: {ex}", exc_info=True)
#             results[log_name] = {
#                 "total_records": 0,
#                 "severity_counts": {},
#                 "error": str(ex)
#             }

#     return results


import logging
from celery import shared_task
import win32evtlog # Older, more stable API
import win32security, win32api
import ntsecuritycon as con
import xml.etree.ElementTree as ET # Still useful for parsing XML data

logger = logging.getLogger(__name__)

# ------------------------
# Enable SeSecurityPrivilege
# ------------------------
def enable_privilege(priv):
    try:
        flags = con.SE_PRIVILEGE_ENABLED
        htoken = win32security.OpenProcessToken(
            win32api.GetCurrentProcess(),
            con.TOKEN_ADJUST_PRIVILEGES | con.TOKEN_QUERY
        )
        luid = win32security.LookupPrivilegeValue(None, priv)
        win32security.AdjustTokenPrivileges(htoken, 0, [(luid, flags)])
        logger.info(f"Privilege enabled: {priv}")
    except Exception as e:
        logger.warning(f"Could not enable privilege {priv}: {e}")

# ------------------------
# Celery task
# ------------------------
@shared_task(time_limit=3600)
def process_windows_event_logs(log_types=None):
    if log_types is None:
        log_types = ["Application", "System", "Setup", "Security"]

    results = {}

    # EventType mapping for win32evtlog
    severity_map = {
        win32evtlog.EVENTLOG_SUCCESS: "Information", # Re-mapping for clarity
        win32evtlog.EVENTLOG_INFORMATION_TYPE: "Information",
        win32evtlog.EVENTLOG_WARNING_TYPE: "Warning",
        win32evtlog.EVENTLOG_ERROR_TYPE: "Error",
        win32evtlog.EVENTLOG_AUDIT_SUCCESS: "Audit Success",
        win32evtlog.EVENTLOG_AUDIT_FAILURE: "Audit Failure",
    }

    for log_name in log_types:
        try:
            # The Security log requires special privileges.
            if log_name == "Security":
                enable_privilege(win32security.SE_SECURITY_NAME)

            # Open the event log.
            handle = win32evtlog.OpenEventLog("localhost", log_name)
            total = win32evtlog.GetNumberOfEventLogRecords(handle)
            
            # Initialize severity counts.
            severity_counts = {
                "Critical": 0, "Error": 0, "Warning": 0, 
                "Information": 0, "Audit Success": 0, 
                "Audit Failure": 0, "Unknown": 0
            }
            
            flags = win32evtlog.EVENTLOG_BACKWARDS_READ | win32evtlog.EVENTLOG_SEQUENTIAL_READ
            
            # Read events in batches.
            while True:
                events = win32evtlog.ReadEventLog(handle, flags, 0)
                if not events:
                    break

                for event in events:
                    # The EventType attribute holds the severity level.
                    level = getattr(event, "EventType", None)
                    if level is not None:
                        severity = severity_map.get(level, "Unknown")
                        severity_counts[severity] += 1
                    else:
                        # Fallback for any un-categorized events
                        severity_counts["Unknown"] += 1
            
            results[log_name] = {"total_records": total, "severity_counts": severity_counts}
            win32evtlog.CloseEventLog(handle)

        except Exception as ex:
            logger.error(f"Failed to process {log_name}: {ex}", exc_info=True)
            results[log_name] = {
                "total_records": 0,
                "severity_counts": {},
                "error": str(ex)
            }

    return results
