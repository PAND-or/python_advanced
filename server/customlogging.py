import logging
from functools import wraps


logger = logging.getLogger('stack_logger')
handler = logging.StreamHandler()

formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(module)s - %(message)s')
handler.setFormatter(formatter)
handler.setLevel(logging.DEBUG)
logger.addHandler(handler)
logger.setLevel(logging.DEBUG)


def stack_logging(message=''):

    def decorator(func):
        @wraps(func)
        def wrap(request, *args, **kwrags):
            format_mapping = {
                'func_name': func.__name__,
                'request_data': request.get('data')
            }
            func_call = func(request, *args, **kwrags)
            logger.debug(
                message % format_mapping, stack_info=True
             )
            return func_call
        return wrap
    return decorator


class StackLogging:
    def __init__(self, message=''):
        self._message = message

    def __call__(self, func):
        @wraps(func)
        def wrap(request, *args, **kwrags):
            format_mapping = {
                'func_name': func.__name__,
                'request_data': request.get('data'),
            }
            func_call = func(request, *args, **kwrags)
            logger.debug(
                self._message  % format_mapping, stack_info=True
            )
            return func_call
        return wrap
