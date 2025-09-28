import logging
import time
from datetime import datetime
from django.http import HttpResponseForbidden
from django.http import JsonResponse

# configure logger to write to requests.log
logger = logging.getLogger(__name__)
file_handler = logging.FileHandler("requests.log")   # log file at project root
formatter = logging.Formatter('%(message)s')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)
logger.setLevel(logging.INFO)


class RequestLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        user = request.user if request.user.is_authenticated else "Anonymous"
        logger.info(f"{datetime.now()} - User: {user} - Path: {request.path}")
        return self.get_response(request)


class RestrictAccessByTimeMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Get current server time (24-hour format)
        current_hour = datetime.now().hour

        # Restrict access outside 6 AM – 9 PM (06:00–21:00)
        if current_hour < 6 or current_hour >= 21:
            return HttpResponseForbidden("Chat access is restricted during this time.")

        return self.get_response(request)
    
class OffensiveLanguageMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        # Dictionary to store IP -> list of timestamps
        self.requests_log = {}

    def __call__(self, request):
        # Only check POST requests (messages are usually POST)
        if request.method == "POST":
            ip = self.get_client_ip(request)
            now = time.time()

            # Keep only requests from last 60 seconds
            if ip not in self.requests_log:
                self.requests_log[ip] = []
            self.requests_log[ip] = [
                ts for ts in self.requests_log[ip] if now - ts < 60
            ]

            # Check rate limit (max 5 requests per minute)
            if len(self.requests_log[ip]) >= 5:
                return JsonResponse(
                    {"error": "Too many messages. Please wait a minute."},
                    status=429  # Too Many Requests
                )

            # Log this request timestamp
            self.requests_log[ip].append(now)

        response = self.get_response(request)
        return response

    def get_client_ip(self, request):
        """Helper to get client IP from headers"""
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip
