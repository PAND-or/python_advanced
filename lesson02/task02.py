#!/usr/bin/python3
__author__ = "Андрей Петров"

import json

"""
2. Задание на закрепление знаний по модулю json. Есть файл orders в формате JSON с информацией о заказах. Написать 
скрипт, автоматизирующий его заполнение данными. Для этого:
Создать функцию write_order_to_json(), в которую передается 5 параметров — товар (item), количество (quantity), 
цена (price), покупатель (buyer), дата (date). Функция должна предусматривать запись данных в виде словаря 
в файл orders.json. При записи данных указать величину отступа в 4 пробельных символа;
Проверить работу программы через вызов функции write_order_to_json() с передачей в нее значений каждого параметра. 
"""


def write_order_to_json(item, quantity, price, buyer, date):
    with open('orders.json') as f_n:
        dict_to_json = json.load(f_n)
        print(dict_to_json)
        dict_to_json['orders'].append({
            'item': item,
            'quantity': quantity,
            'price': price,
            'buyer': buyer,
            'date': date,
        })
    with open('orders.json', 'w') as f_w:
        json.dump(dict_to_json, f_w, indent=4)


if __name__ == "__main__":
    write_order_to_json('Банан', 3, 300, 'Pupkin', '08.03.2019')
    write_order_to_json('Яблоко', 2, 700, 'Pupkin', '08.03.2019')
    write_order_to_json('Апельсин', 3, 1200, 'Pupkin', '08.03.2019')
    write_order_to_json('Груша', 4, 500, 'Pupkin', '08.03.2019')
