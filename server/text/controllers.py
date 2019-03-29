from protocol import make_response, make_400
from authentication import login_required, LoginRequired
from log import log
from customlogging import stack_logging, StackLogging



@stack_logging('Function %(func_name)s was called.')
@log
@login_required
def get_upper_text(request):
    data = request.get('data')
    user = request.get('user')
    print('upper')
    if not data or not user:
        return make_400(request)
    return make_response(
        request,
        200,
        data.upper(),
        send_to=user['account_name'],
        send_from=user['account_name'],
    )



@StackLogging('Request body: %(request_data)s')
@log
@LoginRequired()
def get_lower_text(request):
    data = request.get('data')
    user = request.get('user')
    
    print('lower')
    print(data, user)
    if not data or not user:
        return make_400(request)
    return make_response(
        request,
        200,
        data.lower(),
        send_to=user['account_name'],
        send_from=user['account_name'],
    )
