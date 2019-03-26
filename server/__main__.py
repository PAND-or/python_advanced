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

def get_client_fullname(host, port):
    return f'{ host }:{ port }'

parser = createParser()
args = parser.parse_args(sys.argv[1:])


sock = socket.socket()
sock.bind((args.addr, int(args.port)))
sock.listen(5)

requests = []
connections = []



try:
    while True:
        # принимает сообщение клиента;

        client, address = sock.accept()
        client_full_name = get_client_fullname(*address)
        connections.append((client_full_name, client))

        client_sockets = list(map(lambda item: item[1], connections))

        logger.info(f'Client detected {address}')

        rlist, wlist, xlist = select.select(client_sockets, client_sockets, [], 0)

        for client in wlist:
            read_client_host, read_client_port = client.getsockname()
            read_client_fullname = get_client_fullname(
                read_client_host,
                read_client_port
            )
            data = client.recv(1024)
            request = json.loads(data.decode('utf-8'))
            requests.append((read_client_fullname, request))

        print(requests)

        if requests:
            request_client_fullname, request = requests.pop()
            response = handle_client_request(request)

            print(request_client_fullname, request)
            for client in rlist:
                print('2' * 50)
                write_client_host, write_client_port = client.getsockname()
                write_client_fullname = get_client_fullname(
                    write_client_host,
                    write_client_port
                )

                if write_client_fullname != write_client_fullname:
                    response_string = json.dumps(response)
                    client.send(response_string.encode('utf-8'))
                    logger.info(
                        f'Response { response_string } sended to {client.getsockname()}'
                    )

except KeyboardInterrupt:
    logger.info(f"server {address} closed")
    sock.close()
