#!/usr/bin/python3
__author__ = "Андрей Петров"


import sys
import os
import json
import socket
import argparse
import logging
from datetime import datetime

from protocol import (
    validate_request, make_response,
    make_400, make_404
)
from routes import resolve

logger = logging.getLogger('default')
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
handler = logging.FileHandler('default.log')

handler.setFormatter(formatter)
handler.setLevel(logging.DEBUG)

logger.addHandler(handler)
logger.setLevel(logging.DEBUG)


def createParser():
    parser = argparse.ArgumentParser()
    parser.add_argument('-a', '--addr', nargs='?', default='')
    parser.add_argument('-p', '--port',  nargs='?', default='7777')
    return parser


parser = createParser()
args = parser.parse_args(sys.argv[1:])


sock = socket.socket()
sock.bind((args.addr, int(args.port)))
sock.listen(5)


## Без этого не работал код из урока
#os.chdir('server')
#sys.path.append(os.getcwd())
##

try:
    while True:
        # принимает сообщение клиента;
        client, address = sock.accept()
        logger.debug(f'Client detected {address}')

        data = client.recv(1024)
        request = json.loads(
            data.decode('utf-8')
        )

        if validate_request(request):
            controller = resolve(request.get('action'))
            if controller:
                try:
                    response = controller(request)
                except Exception:
                    response = make_response(
                        request, 500,
                        error='Internal server error.'
                    )
            else:
                response = make_404(request)
        else:
            response = make_400(request)

        response_string = json.dumps(response)
        client.send(response_string.encode('utf-8'))
        client.close()
except KeyboardInterrupt:
    sock.close()
