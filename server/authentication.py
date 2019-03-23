from functools import wraps
from protocol import make_response


def login_required(func):
    @wraps(func)
    def wrap(request, *args, **kwrags):
        if request.get('user'):
            return func(request, *args, **kwrags)
        return make_response(request, 403, 'Access denied.')
    return wrap


class LoginRequired:
    def __call__(self, func):
        @wraps(func)
        def wrap(request, *args, **kwrags):
            if request.get('user'):
                return func(request, *args, **kwrags)
            return make_response(request, 403, 'Access denied.')
        return wrap
