#!/usr/bin/python3
__author__ = "Андрей Петров"

import sys
import json
import socket
import argparse
import select




from protocol import (
    validate_request, make_response,
    make_400, make_404
)
from routes import resolve
from server_log_config import logger
from handlers import handle_client_request

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

responses = []
connections = []

try:
    while True:
        # принимает сообщение клиента;
        client, address = sock.accept()
        connections.append(client)

        logger.info(f'Client detected {address}')

        rlist, wlist, xlist = select.select(connections, connections, [], 0)

        for client in connections:
            if client in rlist: #соеденения на запись
                data = client.recv(1024)
                request = json.loads(
                    data.decode('utf-8')
                )
                action_name = request.get('action')
                response = handle_client_request(request)

                if response.get('code') == 400:
                    logger.error(f'Bad Request: { action_name } request: { request }')

                if response.get('code') == 200:
                    responses.append(response)
                response_string = json.dumps(response)
                client.send(response_string.encode('utf-8'))

            if client in wlist: #соеденения слушатели
               if responses:
                   for conn in wlist:
                       response_obj_string = json.dumps(responses)
                       conn.send(response_obj_string.encode('utf-8'))
            if client in xlist:
                pass
        #client.close()
        #logger.info(f"client {address} closed")
except KeyboardInterrupt:
    logger.info(f"server {address} closed")
    sock.close()
