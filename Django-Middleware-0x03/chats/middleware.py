import logging
from datetime import datetime
from django.http import HttpResponseForbidden

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