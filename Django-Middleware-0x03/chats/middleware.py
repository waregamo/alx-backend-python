from datetime import datetime, timedelta
from django.http import HttpResponseForbidden
from django.utils.deprecation import MiddlewareMixin
import os

# Middleware to log each request
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

# Middleware to restrict access by time
class RestrictAccessByTimeMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        current_hour = datetime.now().hour
        if current_hour < 18 or current_hour >= 21:
            return HttpResponseForbidden("Access to chat is only allowed between 6 PM and 9 PM.")
        return self.get_response(request)

# Middleware to limit offensive language / spam-like messages
class OffensiveLanguageMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.message_counts = {}  # Stores request timestamps per IP

    def __call__(self, request):
        if request.method == 'POST' and request.path.startswith('/api/messages/'):
            ip = self.get_client_ip(request)
            now = datetime.now()
            window_start = now - timedelta(minutes=1)

            # Filter out old timestamps
            timestamps = self.message_counts.get(ip, [])
            timestamps = [ts for ts in timestamps if ts > window_start]
            timestamps.append(now)
            self.message_counts[ip] = timestamps

            if len(timestamps) > 5:
                return HttpResponseForbidden("Rate limit exceeded. Max 5 messages per minute allowed.")

        return self.get_response(request)

    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            return x_forwarded_for.split(',')[0]
        return request.META.get('REMOTE_ADDR')

# Middleware to check user role
class RolePermissionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # You can modify this based on your role model (assuming role is in request.user.role)
        if hasattr(request, 'user') and request.user.is_authenticated:
            user_role = getattr(request.user, 'role', None)
            if user_role not in ['admin', 'moderator']:
                return HttpResponseForbidden("You do not have permission to perform this action.")
        return self.get_response(request)






