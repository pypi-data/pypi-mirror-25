from threading import current_thread

try:
    from django.utils.deprecation import MiddlewareMixin
except ImportError:
    # Not required for Django <= 1.9, see:
    # https://docs.djangoproject.com/en/1.10/topics/http/middleware/#upgrading-pre-django-1-10-style-middleware
    MiddlewareMixin = object


class LocalThreadingRequestMiddleware(MiddlewareMixin):
    def process_request(self, request):
        setattr(current_thread, "request", request)

    def process_response(self, request, response):
        if hasattr(current_thread, "request"):
            delattr(current_thread, "request")
        return response
