from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

class LogFileUploadView(APIView):

    def post(self, request):
        uploaded_file = request.FILES.get('file')
        print('file')

        if not uploaded_file:
            return Response({"error": "No file uploaded"}, status=status.HTTP_400_BAD_REQUEST)

        unusual_logs = []

        # Read the file line by line
        for line in uploaded_file:
            line = line.decode('utf-8').strip() 
            print(line) # convert bytes to string
            # Check for unusual patterns (customize as needed)
            if 'ERROR' in line or 'WARN' in line:
                # Example: split timestamp, log level, message
                parts = line.split(' ', 2) 
                 # adjust depending on log format
                log_entry = {
                    "timestamp": parts[0] if len(parts) > 0 else "",
                    "log_level": parts[1] if len(parts) > 1 else "",
                    "message": parts[2] if len(parts) > 2 else line
                }
                unusual_logs.append(log_entry)

        return Response(unusual_logs, status=status.HTTP_200_OK)
