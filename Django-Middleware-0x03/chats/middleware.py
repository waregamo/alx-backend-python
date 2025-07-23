from datetime import datetime
from django.http import HttpResponseForbidden
import os

# 1. Logs every request
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

# 2. Restrict access based on time
class RestrictAccessByTimeMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        current_hour = datetime.now().hour
        if current_hour < 18 or current_hour >= 21:
            return HttpResponseForbidden("Access to chat is only allowed between 6 PM and 9 PM.")
        return self.get_response(request)

# 3. Check for offensive language
class OffensiveLanguageMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.offensive_words = ['badword', 'offensive', 'ugly']  # example words

    def __call__(self, request):
        if request.method == 'POST':
            if hasattr(request, 'body') and request.body:
                body = request.body.decode('utf-8').lower()
                if any(word in body for word in self.offensive_words):
                    return HttpResponseForbidden("Offensive language is not allowed.")
        return self.get_response(request)

# 4. Enforce role permissions
class RolepermissionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        user = request.user
        if hasattr(user, 'role'):
            if user.role not in ['admin', 'moderator']:
                return HttpResponseForbidden("Access denied: Insufficient permissions.")
        else:
            return HttpResponseForbidden("Access denied: Role not defined.")
        return self.get_response(request)






