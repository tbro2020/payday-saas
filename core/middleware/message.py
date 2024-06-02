from django.contrib import messages
from core.message import get_messages

class AsyncMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        """
        try:
            if hasattr(request, "session") and hasattr(request, "user"):
                msgs = get_messages(request.user)
                for msg, level in msgs:
                    messages.add_message(request, level, msg)
        except:
            print("failed to fetch message")
        """
        return self.get_response(request)
