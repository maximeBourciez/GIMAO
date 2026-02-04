import threading


_thread_locals = threading.local()

def get_current_request():
    return getattr(_thread_locals, 'request', None)

def get_current_user():
    request = get_current_request()
    if request:
        return getattr(request, 'user', None)
    return None


def set_thread_user(user):
    _thread_locals.app_user = user

def get_thread_user():
    return getattr(_thread_locals, 'app_user', None)

class CurrentUserMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # We process request but we might rely on ViewSet to set the user
        # However, for non-ViewSet requests (admin?), we might still want to capture request
        _thread_locals.request = request
        response = self.get_response(request)
        if hasattr(_thread_locals, 'request'):
            del _thread_locals.request
        if hasattr(_thread_locals, 'app_user'):
            del _thread_locals.app_user
        return response
