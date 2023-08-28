"""
Первое задание.

Нужно было вывести данные в соответствии с их вложенностью в словаре используя функцию
"""


def my_code(data_set: dict, iter=0):  # Сама функция
    keys = data_set.keys()  # Получаем ключи словаря
    for key in keys:  # Проходимся по ключам
        print(('\t' * iter) + key+':')  # Выводим ключи
        if type(data_set.get(key)) == dict:  # Проверка типа данных
            my_code(data_set.get(key), iter + 1)  # Передаём новые значения в имеющуюся функцию (рекурсия)
        else:
            print(('\t' * (iter + 1))+data_set.get(key))  # Выводим с учетом количества итераций рекурсии (табуляция)


data_set_1 = {
    'first': 'first_value',
    'second': 'second_value'
}  # Наборы данных для проверки

data_set_2 = {
    '1': {
        'child': '1/child/value'
    },
    '2': {
        'child': '2/child/value'
    }
}

my_code(data_set_1)  # вызов функции
my_code(data_set_2)
