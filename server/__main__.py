#!/usr/bin/python3
__author__ = "Андрей Петров"

import sys
import json
from socket import socket, AF_INET, SOCK_STREAM
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


def read_requests(r_clients, all_clients):
   """ Чтение запросов из списка клиентов
   """
   responses = {}  # Словарь ответов сервера вида {сокет: запрос}
   #print('read_requests')
   for sock in r_clients:
       try:
           print('client 1')
           data = sock.recv(1024).decode('utf-8')
           responses[sock] = json.loads(data)
           print(responses[sock])
       except:
           print('Клиент {} {} отключился'.format(sock.fileno(), sock.getpeername()))
           all_clients.remove(sock)

   return responses


def write_responses(requests, w_clients, all_clients):
   """ Эхо-ответ сервера клиентам, от которых были запросы
   """

   for sock in w_clients:
       if sock in requests:
           #print('write_responses')
           response = handle_client_request(requests[sock])
           response_string = json.dumps(response)

           try:
               # Подготовить и отправить ответ сервера
                print('Сообщение отправлено')
                sock.send(response_string.encode('utf-8'))
           except:  # Сокет недоступен, клиент отключился
               print('Клиент {} {} отключилсяя'.format(sock.fileno(), sock.getpeername()))
               #sock.close()
               #all_clients.remove(sock)



parser = createParser()
args = parser.parse_args(sys.argv[1:])


sock = socket(AF_INET, SOCK_STREAM)
sock.bind((args.addr, int(args.port)))
sock.listen(5)
sock.settimeout(0.2)

requests = []
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

                #print('r:', len(r), ' w:', len(w), ' e:', len(e))
                requests = read_requests(r, clients)  # Сохраним запросы клиентов
                if requests:
                    write_responses(requests, w, clients)  # Выполним отправку ответов
            except:
                pass  # Ничего не делать, если какой-то клиент отключился



except KeyboardInterrupt:
    #logger.info(f"server {address} closed")
    sock.close()
