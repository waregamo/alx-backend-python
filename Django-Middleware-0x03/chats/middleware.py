# chats/middleware.py

from datetime import datetime
from django.http import HttpResponseForbidden
import os


class RequestLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        # Define log file path (store in root directory)
        self.log_file = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'requests.log')

    def __call__(self, request):
        user = request.user.username if hasattr(request, 'user') and request.user.is_authenticated else 'Anonymous'
        log_message = f"{datetime.now()} - User: {user} - Path: {request.path}\n"

        with open(self.log_file, 'a') as file:
            file.write(log_message)

        return self.get_response(request)


class RestrictAccessByTimeMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        current_hour = datetime.now().hour
        # Allow only between 6 PM and 9 PM (18:00 - 21:00)
        if current_hour < 18 or current_hour >= 21:
            return HttpResponseForbidden("Access to chat is only allowed between 6 PM and 9 PM.")
        return self.get_response(request)






