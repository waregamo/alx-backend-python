from datetime import datetime, timedelta
from django.http import HttpResponseForbidden
from django.utils.deprecation import MiddlewareMixin
import os
from collections import defaultdict


class RequestLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
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


class OffensiveLanguageMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.message_log = defaultdict(list)  # {ip: [timestamp1, timestamp2, ...]}

    def __call__(self, request):
        if request.method == 'POST' and request.path.startswith('/api/messages'):
            ip = self.get_client_ip(request)
            now = datetime.now()

            # Clean up timestamps older than 1 minute
            self.message_log[ip] = [ts for ts in self.message_log[ip] if now - ts < timedelta(minutes=1)]

            if len(self.message_log[ip]) >= 5:
                return HttpResponseForbidden("Message limit exceeded. Please wait before sending more.")

            self.message_log[ip].append(now)

        return self.get_response(request)

    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip






