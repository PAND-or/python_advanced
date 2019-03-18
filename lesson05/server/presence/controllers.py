from protocol import make_response, make_400


def send_presence(request):
    user = request.get('user')
    if not user:
        return make_400(request)
    return make_response(
        request,
        200,
        alert=f"Hi {user['account_name']}"
    )
