from protocol import make_response, make_400
from authentication import login_required, LoginRequired
from log import log
from customlogging import stack_logging, StackLogging



@stack_logging('Function %(func_name)s was called.')
@log
@login_required
def get_upper_text(request):
    data = request.get('data')
    if not data:
        return make_400(request)
    return make_response(
        request,
        200,
        data.upper()
    )



@StackLogging('Request body: %(request_data)s')
@log
@LoginRequired()
def get_lower_text(request):
    data = request.get('data')
    if not data:
        return make_400(request)
    return make_response(
        request,
        200,
        data.lower()
    )
