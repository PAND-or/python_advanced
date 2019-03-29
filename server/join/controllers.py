from protocol import make_response, make_400
from log import log

@log
def jim_join(request):
    room = request.get('room')
    user = request.get('user')
    print('jim_join')
    if not user or not room:
        return make_400(request)
    return make_response(
        request,
        200,
        send_to=room,
        send_from=user['account_name'],
        alert=f"{user['account_name']} join the room: {room} "
    )
