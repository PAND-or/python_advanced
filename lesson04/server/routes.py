import os
from importlib import import_module
from functools import reduce


def get_server_routes():
    return reduce(
        lambda routes, module: routes + getattr(module, 'routes', []),
        reduce(
            lambda modules, dir: modules + [import_module(f'{dir}.routes')],
            filter(
                lambda itm: os.path.isdir(itm) and itm != '__pycache__' and itm != '.pytest_cache',
                os.listdir()
            ),
            []
        ),
        []
    )


