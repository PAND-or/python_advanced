#!/usr/bin/python3
__author__ = "Андрей Петров"

import sys
import json
from socket import socket, AF_INET, SOCK_STREAM
import argparse
import select
import threading
import collections


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


def read_requests(sock, allclients):
   """ Чтение запросов из списка клиентов
   """
   #responses = []
   #print('read_requests')
#for sock in r_clients:
   try:
       data = sock.recv(1024).decode('utf-8')
       #responses[sock] = json.loads(data)
       #print(responses[sock])
       requests.append(json.loads(data))
       #print(requests[sock])
   except:
       print('Клиент {} {} отключился'.format(sock.fileno(), sock.getpeername()))
       clients.remove(sock)

  #return responses


def write_responses(req, sock, all_clients):
#for req in requests:
        #print('write_responses')
        #print(req)
        # Разобрать все запросы
        response = handle_client_request(req)
        response_string = json.dumps(response)
    #for sock in w_clients:
        try:
            # отправить всем
            sock.send(response_string.encode('utf-8'))
            #print('Сообщение отправлено')
        except:  # Сокет недоступен, клиент отключился
           print('Клиент {} {} отключился'.format(sock.fileno(), sock.getpeername()))
           #sock.close()
           #all_clients.remove(sock)


parser = createParser()
args = parser.parse_args(sys.argv[1:])


sock = socket(AF_INET, SOCK_STREAM)
sock.bind((args.addr, int(args.port)))
sock.listen(5)
sock.settimeout(0.2)

requests = collections.deque()
responses = collections.deque()
connections = []
clients = []

try:
    while True:
        try:
            conn, addr = sock.accept()  # Проверка подключений
        except OSError as e:
            pass  # timeout вышел
        else:
            print("Получен запрос на соединение от %s" % str(addr))
            clients.append(conn)
        finally:
            # Проверить наличие событий ввода-вывода
            wait = 0
            r = []
            w = []


            try:
                r, w, e = select.select(clients, clients, [], wait)


                for sock in r:
                    #print('r:', len(r), ' w:', len(w), ' e:', len(e))
                    read_thred = threading.Thread(
                        target=read_requests, args=(sock, clients),
                    )
                    read_thred.start()

                # requests = read_requests(r, clients)  # Сохраним запросы клиентов
                if requests:
                    request = requests.popleft()
                    for sock in w:
                        write_thred = threading.Thread(
                            target=write_responses, args=(request, sock, clients)
                        )
                        write_thred.start()
                    #write_responses(requests, w, clients)  # Выполним отправку ответов
            except:
                pass  # Ничего не делать, если какой-то клиент отключился



except KeyboardInterrupt:
    #logger.info(f"server {address} closed")
    sock.close()
