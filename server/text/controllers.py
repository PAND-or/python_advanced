from protocol import make_response, make_400
from log import log


@log
def get_upper_text(request):
    data = request.get('data')
    if not data:
        return make_400(request)
    return make_response(
        request,
        200,
        data.upper()
    )

@log
def get_lower_text(request):
    data = request.get('data')
    if not data:
        return make_400(request)
    return make_response(
        request,
        200,
        data.lower()
    )
