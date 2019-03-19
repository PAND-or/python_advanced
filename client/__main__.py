#!/usr/bin/python3
__author__ = "Андрей Петров"

"""
клиент отправляет запрос серверу;
сервер отвечает соответствующим кодом результата. Клиент и сервер должны быть реализованы в виде отдельных скриптов, 
содержащих соответствующие функции. 

Функции клиента: 
сформировать presence-сообщение; 
отправить сообщение серверу; 
получить ответ сервера;
разобрать сообщение сервера; 
параметры командной строки скрипта client.py <addr> [<port>]: addr — ip-адрес сервера; 
port — tcp-порт на сервере, 
по умолчанию 7777. 

"""
import re
import sys
import argparse
import socket
import json
from datetime import datetime
from client_log_config import logger


def createParser():
    parser = argparse.ArgumentParser()
    parser.add_argument('host', nargs='?', default='localhost')
    parser.add_argument('port',  nargs='?', default='7777')
    return parser



parser = createParser()
args = parser.parse_args(sys.argv[1:])

port = int(re.search('[0-9]{2,}', args.port).group(0))


sock = socket.socket()
try:
    sock.connect((args.host, port))

    # сформировать presence-сообщение;
    # В формате JIM

    msg_presence = json.dumps(
        {
            "action": "presence",
            "time": datetime.now().timestamp(),
            "type": "status",
            "user": {
                    "account_name":  input("Enter user Name: "),
                    "status": input("Status message: ")
            }
        }
    )
    """
    msg_action = json.dumps(
        {
            "action": input("Enter action (lower_text): "),
            "data": input("Enter data: ")
        }
    )
    #sock.send(msg_action.encode())
    """

    # отправить сообщение серверу;
    sock.send(msg_presence.encode())


    # получить ответ сервера;
    data = sock.recv(1024)
    response = json.loads(
        data.decode('utf-8')
    )
    # разобрать сообщение сервера;

    if response.get('response') == 200:
        if response.get('alert'):
            logger.debug(f"Response Message: {response.get('alert')}")
            print(
                f"Response Message: {response.get('alert')}"
            )
    else:
        logger.critical(f"Error request: {response.get('error')}")

    sock.close()
except Exception:
    logger.critical(f'client cant conntect to host:{args.host} port{port}')
