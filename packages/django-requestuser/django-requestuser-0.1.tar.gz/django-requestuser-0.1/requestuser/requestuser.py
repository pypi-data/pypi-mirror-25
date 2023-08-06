import threading
from django.utils.deprecation import MiddlewareMixin


_active = threading.local()


def activate(user):
    if user.is_anonymous():
        _active.user = None
    else:
        _active.user = user.pk


def get_request_user():
    from django.contrib.auth import get_user_model
    from django.contrib.auth.models import AnonymousUser
    if not hasattr(_active, 'user') or _active.user is None:
        user = AnonymousUser()
    else:
        User = get_user_model()
        user = User.objects.get(pk=_active.user)
    return user


class RequestUserMiddleware(MiddlewareMixin):

    def process_request(self, request):
        activate(request.user)

    '''
    def process_response(self, request, response):
        return response
    '''
