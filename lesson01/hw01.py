#!/usr/bin/python3
__author__ = "Андрей Петров"


"""
1. Каждое из слов «разработка», «сокет», «декоратор» представить в строковом формате и проверить тип и содержание 
соответствующих переменных. Затем с помощью онлайн-конвертера преобразовать строковые представление в формат Unicode 
и также проверить тип и содержимое переменных.

>>> a = 'разработка'
>>> print(f'development: {a}, type {type(a)}')
development: разработка, type <class 'str'>

>>> b = 'сокет'
>>> print(f'socket: {b}, type {type(b)}')
socket: сокет, type <class 'str'>

>>> c = 'декоратор'
>>> print(f'decorator: {c}, type {type(c)}')
decorator: декоратор, type <class 'str'>

>>> a = a.encode('utf-8')
>>> print(f'development: {a}, type {type(a)}')
development: b'\xd1\x80\xd0\xb0\xd0\xb7\xd1\x80\xd0\xb0\xd0\xb1\xd0\xbe\xd1\x82\xd0\xba\xd0\xb0', type <class 'bytes'>

>>> b = b.encode('utf-8')
>>> print(f'socket: {b}, type {type(b)}')
socket: b'\xd1\x81\xd0\xbe\xd0\xba\xd0\xb5\xd1\x82', type <class 'bytes'>

>>> c = c.encode('utf-8')
>>> print(f'decorator: {c}, type {type(c)}')
decorator: b'\xd0\xb4\xd0\xb5\xd0\xba\xd0\xbe\xd1\x80\xd0\xb0\xd1\x82\xd0\xbe\xd1\x80', type <class 'bytes'>

"""


"""
2. Каждое из слов «class», «function», «method» записать в байтовом типе без преобразования в последовательность кодов 
(не используя методы encode и decode) и определить тип, содержимое и длину соответствующих переменных.

>>> a = b'class'
>>> print(f'class: {a}, type: {type(a)}, len:{len(a)}')
class: b'class', type: <class 'bytes'>, len:5

>>> b = b'function'
>>> print(f'function: {b}, type: {type(b)}, len:{len(b)}')
function: b'function', type: <class 'bytes'>, len:8

>>> c = b'method'
>>> print(f'method: {c}, type: {type(c)}, len:{len(c)}')
method: b'method', type: <class 'bytes'>, len:6
"""


"""
3. Определить, какие из слов «attribute», «класс», «функция», «type» невозможно записать в байтовом типе.

>>> b'attribute'
b'attribute'

>>> b'класс'
  File "<input>", line 1
SyntaxError: bytes can only contain ASCII literal characters.

>>> b'функция'
  File "<input>", line 1
SyntaxError: bytes can only contain ASCII literal characters.

>>> b'type'
b'type'

Нельзя записать в байтовый тип без преобразования кириллические символы, т.к. на хранение одного 
кириллическоно символа требуется больше 1 байта

"""


"""
4. Преобразовать слова «разработка», «администрирование», «protocol», «standard» из строкового представления в байтовое
 и выполнить обратное преобразование (используя методы encode и decode).
 
>>> a = 'разработка'
>>> a
'разработка'
>>> a = a.encode()
>>> a
b'\xd1\x80\xd0\xb0\xd0\xb7\xd1\x80\xd0\xb0\xd0\xb1\xd0\xbe\xd1\x82\xd0\xba\xd0\xb0'
>>> a = a.decode()
>>> a
'разработка'

>>> b = 'администрирование'
>>> b
'администрирование'
>>> b = b.encode()
>>> b
b'\xd0\xb0\xd0\xb4\xd0\xbc\xd0\xb8\xd0\xbd\xd0\xb8\xd1\x81\xd1\x82\xd1\x80\xd0\xb8\xd1\x80\xd0\xbe\xd0\xb2\xd0\xb0\xd0\xbd\xd0\xb8\xd0\xb5'
>>> b = b.decode()
>>> b
'администрирование'

>>> c = 'protocol'
>>> c
'protocol'
>>> c = c.encode()
>>> c
b'protocol'
>>> c = c.decode()
>>> c
'protocol'

>>> d = 'standard'
>>> d
'standard'
>>> d = d.encode()
>>> d
b'standard'
>>> d = d.decode()
>>> d
'standard'

"""

"""
5. Выполнить пинг веб-ресурсов yandex.ru, youtube.com и преобразовать результаты из байтовового 
в строковый тип на кириллице.

>>> import subprocess
>>> args = ['ping', 'yandex.ru']
>>> subproc_ping = subprocess.Popen(args, stdout=subprocess.PIPE)
>>> for line in subproc_ping.stdout:
...     line = line.decode('cp866').encode('utf-8')
...     print(line.decode('utf-8'))         
... 
Ответ от 5.255.255.70: число байт=32 время=24мс TTL=57
Ответ от 5.255.255.70: число байт=32 время=26мс TTL=57
Ответ от 5.255.255.70: число байт=32 время=27мс TTL=57

Статистика Ping для 5.255.255.70:
    Пакетов: отправлено = 4, получено = 4, потеряно = 0
    (0% потерь)
Приблизительное время приема-передачи в мс:
    Минимальное = 24мсек, Максимальное = 27 мсек, Среднее = 25 мсек
    
    
>>> args = ['ping', 'youtube.com']
>>> subproc_ping = subprocess.Popen(args, stdout=subprocess.PIPE)
>>> for line in subproc_ping.stdout: 
...     line = line.decode('cp866').encode('utf-8')
...     print(line.decode('utf-8'))
...     
Обмен пакетами с youtube.com [173.194.44.39] с 32 байтами данных:
Ответ от 173.194.44.39: число байт=32 время=23мс TTL=120
Ответ от 173.194.44.39: число байт=32 время=22мс TTL=120
Ответ от 173.194.44.39: число байт=32 время=21мс TTL=120
Ответ от 173.194.44.39: число байт=32 время=23мс TTL=120

Статистика Ping для 173.194.44.39:
    Пакетов: отправлено = 4, получено = 4, потеряно = 0
    (0% потерь)
Приблизительное время приема-передачи в мс:
    Минимальное = 21мсек, Максимальное = 23 мсек, Среднее = 22 мсек

"""

"""
6. Создать текстовый файл test_file.txt, заполнить его тремя строками: «сетевое программирование», «сокет», 
«декоратор». Проверить кодировку файла по умолчанию. Принудительно открыть файл в формате Unicode и 
вывести его содержимое.

>>> with open('E:/PythonScripts/Repo/python_advanced/lesson01/test_file.txt') as file:
...     for f_str in file:         
...          print(f_str)
...      
п»їСЃРµС‚РµРІРѕРµ РїСЂРѕРіСЂР°РјРјРёСЂРѕРІР°РЅРёРµ
СЃРѕРєРµС‚
РґРµРєРѕСЂР°С‚РѕСЂ

>>> with open('E:/PythonScripts/Repo/python_advanced/lesson01/test_file.txt', encoding='utf-8') as file:
...     for f_str in file:         
...          print(f_str)
...      
﻿сетевое программирование
сокет
декоратор

"""
