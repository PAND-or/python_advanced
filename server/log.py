""""
2. В декораторе @log реализовать фиксацию функции, из которой была вызвана декорированная. Если имеется такой код:
@log
def func_z():
 pass

def main():
 func_z()
...в логе должна быть отражена информация:
"<дата-время> Функция func_z() вызвана из функции main"
"""

import inspect
from server_log_config import logger

def log(func):
    def wrap(request, *args, **kwargs):
        file_name = inspect.currentframe().f_back.f_code.co_filename
        mname = inspect.getmodulename(file_name)
        logger.info(f'function  {func.__name__}{args} call from {mname}')
        return func(request, *args, **kwargs)
    return wrap
