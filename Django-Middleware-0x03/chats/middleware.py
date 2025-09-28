from datetime import datetime
from django.http import HttpResponseForbidden

class RestrictAccessByTimeMiddleware:
    """
    Middleware that restricts access to the chat app
    outside of allowed hours (6AM – 9PM).
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Get current hour (24-hour format)
        current_hour = datetime.now().hour

        # Deny access if time is between 9PM (21) and 6AM (6)
        if current_hour >= 21 or current_hour < 6:
            return HttpResponseForbidden(
                "Access to the chat is restricted between 9PM and 6AM."
            )

        # Continue normally if within allowed hours
        return self.get_response(request)

