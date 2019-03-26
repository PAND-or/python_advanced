from datetime import datetime


def validate_request(raw):
    #print(raw)
    request_time = raw.get('time')
    request_action = raw.get('action')
    if request_time and request_action:
        return True
    return False


def make_response(request, code, data=None, error=None, alert=None):
    return {
        'action': request.get('action'),
        'user': request.get('user'),
        'time': datetime.now().timestamp(),
        'data': data,
        'response': code,
        'error': error,
        'alert': alert,
    }


def make_400(request):
    return make_response(request, 400, error='Wrong request format')


def make_404(request):
    return make_response(request, 404, error='Action is not supported.')
