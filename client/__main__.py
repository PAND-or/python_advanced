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
import hashlib
from datetime import datetime
from client_log_config import logger
import select


def createParser():
    parser = argparse.ArgumentParser()
    parser.add_argument('host', nargs='?', default='localhost')
    parser.add_argument('port',  nargs='?', default='7777')
    parser.add_argument('-m', '--mode', nargs='?', type=str, default='w')
    return parser



parser = createParser()
args = parser.parse_args(sys.argv[1:])

port = int(re.search('[0-9]{2,}', args.port).group(0))

try:
    sock = socket.socket()
    sock.connect((args.host, port))

    if args.mode == 'w':
        while True:
            # сформировать presence-сообщение;
            # В формате JIM

            hash_obj = hashlib.sha1()
            hash_obj.update(b'secret_key')

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
            # отправить сообщение серверу;
            sock.send(msg_presence.encode())
            """
            msg_action = json.dumps(
                {
                    "action": input("Enter action (lower_text): "),
                    "data": input("Enter data: ")
                }
            )
        
            sock.send(msg_action.encode())
             """

    else:
        while True:
            rlist, wlist, xlist = select.select([], [sock], [], 0)

            response = sock.recv(1024)

            if response:
                print(response.decode())
                break
except KeyboardInterrupt:
    logger.info(f"client closed")
    sock.close()

except Exception:
    logger.critical(f'client cant conntect to host:{args.host} port{port}')
