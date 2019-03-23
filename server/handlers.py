from protocol import (
    validate_request, make_response,
    make_400, make_404
)
from routes import resolve
from server_log_config import logger


def handle_client_request(request):
    if validate_request(request):
        controller = resolve(request.get('action'))
        if controller:
            try:
                return controller(request)
            except Exception as err:
                logger.critical(err, exc_info=True)
                return make_response(
                    request, 500,
                    error='Internal server error.'
                )
        else:
            logger.critical(f"error 404 controller: {request.get('action')} not found")
            return make_404(request)
    else:
        logger.critical(f"error 400 bad request: {request}")
        return make_400(request)

