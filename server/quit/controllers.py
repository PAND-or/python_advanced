from protocol import make_response, make_400
from log import log

@log
def jim_quit(request):
    user = request.get('user')

    if not user:
        return make_400(request)
    return make_response(
        request,
        200,
        send_to=user['account_name'],
        send_from=user['account_name'],
        alert=f"{user['account_name']} quit "
    )
