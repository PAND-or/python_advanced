#!/usr/bin/python3
__author__ = "Андрей Петров"

import sys



import json
import socket
import argparse





from protocol import (
    validate_request, make_response,
    make_400, make_404
)
from routes import resolve
from server_log_config import logger

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
                    logger.critical(f'error 500 controller: {controller}')
                    response = make_response(
                        request, 500,
                        error='Internal server error.'
                    )
            else:
                logger.critical(f"error 404 controller: {request.get('action')} not found")
                response = make_404(request)
        else:
            response = make_400(request)
            logger.critical(f"error 400 bad request: {request}")

        response_string = json.dumps(response)
        client.send(response_string.encode('utf-8'))
        client.close()
        logger.debug(f"client {address} closed")
except KeyboardInterrupt:
    sock.close()
