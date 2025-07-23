# chats/middleware.py

from datetime import datetime
import os

class RequestLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        # Define log file path (in project root)
        self.log_file = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'requests.log')

    def __call__(self, request):
        user = request.user if hasattr(request, 'user') and request.user.is_authenticated else 'Anonymous'
        log_message = f"{datetime.now()} - User: {user} - Path: {request.path}\n"

        with open(self.log_file, 'a') as file:
            file.write(log_message)

        response = self.get_response(request)
        return response
