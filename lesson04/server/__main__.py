#!/usr/bin/python3
__author__ = "Андрей Петров"

"""
клиент отправляет запрос серверу;
сервер отвечает соответствующим кодом результата. Клиент и сервер должны быть реализованы в виде отдельных скриптов, 
содержащих соответствующие функции. 

Функции сервера: 
принимает сообщение клиента; 
формирует ответ клиенту; 
отправляет ответ клиенту; 
имеет параметры командной строки: -p <port> — TCP-порт для работы (по умолчанию использует 7777); 
-a <addr> — IP-адрес для прослушивания (по умолчанию слушает все доступные адреса).
"""

import sys
import os
import json
import socket
import argparse
from routes import get_server_routes


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
os.chdir('server')
sys.path.append(os.getcwd())
##

while True:
    # принимает сообщение клиента;
    client, address = sock.accept()

    data = client.recv(1024)
    request = json.loads(
        data.decode('utf-8')
    )

    # формирует ответ клиенту;

    client_action = request.get('action')

    resolved_routes = list(
        filter(
            lambda itm: itm.get('action') == client_action,
            get_server_routes()
        )
    )

    route = resolved_routes[0] if resolved_routes else None
    if route:
        controller = route.get('controller')
        response = controller(request.get('data'), request)

    else:
        response = {
            "response": 400,
            "error": "Wrong action, try again"
        }

    # отправляет ответ клиенту;
    client.send(json.dumps(response).encode('utf-8'))
    client.close()
