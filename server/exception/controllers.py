from protocol import make_response, make_400
from log import log

@log
def get_error(request):
    raise Exception('Some test error')