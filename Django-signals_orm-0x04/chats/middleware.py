import logging
from datetime import datetime
from django.http import HttpResponseForbidden
from datetime import datetime
import time
from django.http import JsonResponse


logger = logging.getLogger(__name__)
handler = logging.FileHandler("requests.log")
formatter = logging.Formatter('%(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.INFO)

class RequestLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        user = request.user if request.user.is_authenticated else "Anonymous"
        log_message = f"{datetime.now()} - User: {user} - Path: {request.path}"
        logger.info(log_message)

        response = self.get_response(request)
        return response


class RestrictAccessByTimeMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        current_hour = datetime.now().hour
        if not (6 <= current_hour <= 21):  # Between 6AM and 9PM
            return HttpResponseForbidden("Chat access is restricted during this time.")
        return self.get_response(request)

class OffensiveLanguageMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.message_log = {}  # IP: [timestamps]

    def __call__(self, request):
        ip = self.get_client_ip(request)
        current_time = time.time()

        # Check rate limiting
        if request.method == "POST" and request.path.startswith("/messages"):
            timestamps = self.message_log.get(ip, [])
            timestamps = [t for t in timestamps if current_time - t < 60]  # last 60 sec
            if len(timestamps) >= 5:
                return JsonResponse(
                    {"error": "Rate limit exceeded. Max 5 messages per minute."},
                    status=429
                )
            timestamps.append(current_time)
            self.message_log[ip] = timestamps

            # Optional: Offensive language detection (basic example)
            body = request.body.decode('utf-8').lower()
            offensive_words = ['badword', 'ugly', 'stupid']
            if any(word in body for word in offensive_words):
                return JsonResponse({"error": "Offensive language detected."}, status=400)

        return self.get_response(request)

    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            return x_forwarded_for.split(',')[0]
        return request.META.get('REMOTE_ADDR')


class RolepermissionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        protected_paths = ['/admin-action/', '/messages/delete/']

        if request.path in protected_paths:
            if not request.user.is_authenticated or request.user.role not in ['admin', 'moderator']:
                return JsonResponse({"error": "You don't have permission to perform this action."}, status=403)

        return self.get_response(request)