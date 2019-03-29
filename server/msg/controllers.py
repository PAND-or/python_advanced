from protocol import make_response, make_400
from log import log

@log
def jim_msg(request):
    request_to = request.get('to')
    request_from = request.get('from')
    user = request.get('user')
    print('jim_msg')

    message = request.get('message')

    if not user or not request_to or not request_from:
        return make_400(request)
    return make_response(
        request,
        200,
        send_to=request_to,
        send_from=request_from,
        alert=f"{user['account_name']}: {message} "
    )

