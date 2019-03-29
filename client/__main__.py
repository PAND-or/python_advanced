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
from socket import socket, AF_INET, SOCK_STREAM
import json
import hashlib
from datetime import datetime
from client_log_config import logger
import select


def create_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('host', nargs='?', default='localhost')
    parser.add_argument('port',  nargs='?', default='7777')
    parser.add_argument('-m', '--mode', nargs='?', type=str, default='w')
    return parser


def read_response(response, mode='w'):
    response = json.loads(
        data.decode('utf-8')
    )
    # разобрать сообщение сервера;

    if response.get('response') == 200:
        if response.get('alert'):
            if mode == 'w':
                logger.debug(f"Response Message: {response.get('alert')}")
                print(
                    f"{response.get('alert')}"
                )
            else:
                print(
                    f"{response.get('user')['account_name']}: {response.get('user')['status']}\n",
                    f"{response.get('alert')}"
                )
    else:
        logger.critical(f"Error request: {response.get('error')}")


parser = create_parser()
args = parser.parse_args(sys.argv[1:])

port = int(re.search('[0-9]{2,}', args.port).group(0))



try:
    sock = socket(AF_INET, SOCK_STREAM)
    sock.connect((args.host, port))

    if args.mode == 'w':
        username = input("Enter user Name: ")
        while True:
            # сформировать presence-сообщение;
            # В формате JIM

            hash_obj = hashlib.sha1()
            hash_obj.update(b'secret_key')

            user = {
                "account_name":  username,
                "status": 'Online'
            }

            msg_presence = json.dumps(
                {
                    "action": "presence",
                    "time": datetime.now().timestamp(),
                    "type": "status",
                    "user": user
                }
            )
            sock.send(msg_presence.encode())
            data = sock.recv(1024)

            while True:
                action = input("Enter action (chat, p2p, text, exit): ")
                if action == 'exit':
                    logger.info(f"client closed")
                    sock.close()
                    break
                elif action == 'text':
                    msg_action = json.dumps(
                        {
                            "action": input("Enter action (lower_text, upper_text): "),
                            "data": input("Enter data: "),
                            "user": user
                        }
                    )
                    sock.send(msg_action.encode())
                    # получить ответ сервера;
                    data = sock.recv(1024)
                    read_response(data)
                elif action == 'chat':
                    join_request = json.dumps(
                        {
                            "action": "join",
                            "time": datetime.now().timestamp(),
                            "room": "#common",
                            "user": user
                        }
                    )
                    sock.send(join_request.encode())
                    data = sock.recv(1024)
                    while True:
                        message = input("Enter message (or exit): ")
                        if message == 'exit':
                            leave_request = json.dumps(
                                {
                                    "action": "leave",
                                    "time": datetime.now().timestamp(),
                                    "room": "#common",
                                    "user": user
                                }
                            )
                            sock.send(leave_request.encode())
                            break
                        chat_request = json.dumps({
                            "action": "msg",
                            "time": datetime.now().timestamp(),
                            "to": '#common',
                            "from": username,
                            "encoding": "utf-8",
                            "message": message,
                            "user": user
                        })
                        # отправить сообщение серверу;
                        sock.send(chat_request.encode())
                        # получить ответ сервера;
                        data = sock.recv(1024)
                        read_response(data)
                elif action == 'p2p':
                    sendto = input("Enter user_name for send: ")
                    while True:
                        message = input("Enter message (or exit): ")
                        if message == 'exit':
                            break

                        p2p_request = json.dumps({
                            "action": "msg",
                            "time": datetime.now().timestamp(),
                            "to": sendto,
                            "from": username,
                            "encoding": "utf-8",
                            "message": message,
                            "user": user
                        })
                        # отправить сообщение серверу;
                        sock.send(p2p_request.encode())
                        # получить ответ сервера;
                        data = sock.recv(1024)
                        read_response(data)
    else:
        while True:  # Постоянный опрос сервера
            data = sock.recv(1024)
            read_response(data, 'r')
        #sock.close()
except KeyboardInterrupt:
    logger.info(f"client closed")
    sock.close()

except Exception:
    logger.critical(f'client cant conntect to host:{args.host} port{port}')
